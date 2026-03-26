#!/usr/bin/env python3
"""
Coded using Claude Sonnet 4.6.
scan_document.py — Turn a photo of a document into a flat, rectangular "scan".

Usage:
    python scan_document.py input.jpg                  # saves as input_scanned.jpg
    python scan_document.py input.jpg -o output.jpg    # custom output path
    python scan_document.py *.jpg                      # batch mode
    python scan_document.py input.jpg --show           # preview result
    python scan_document.py input.jpg --debug          # show intermediate steps

Requirements:
    pip install opencv-python-headless numpy
    (use opencv-python instead if you want GUI windows)
"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np


# ---------------------------------------------------------------------------
# Core geometry helpers
# ---------------------------------------------------------------------------

def order_points(pts):
    """Return points in order: top-left, top-right, bottom-right, bottom-left."""
    pts = np.array(pts, dtype="float32")
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # top-left  (smallest x+y)
    rect[2] = pts[np.argmax(s)]   # bot-right (largest  x+y)

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right (smallest y-x)
    rect[3] = pts[np.argmax(diff)]  # bot-left  (largest  y-x)

    return rect


def four_point_transform(image, pts):
    """Warp the quadrilateral defined by pts into a flat rectangle."""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Compute output width (longest of the two horizontal edges)
    width_top    = np.linalg.norm(tr - tl)
    width_bottom = np.linalg.norm(br - bl)
    width = int(max(width_top, width_bottom))

    # Compute output height (longest of the two vertical edges)
    height_left  = np.linalg.norm(bl - tl)
    height_right = np.linalg.norm(br - tr)
    height = int(max(height_left, height_right))

    dst = np.array([
        [0,         0         ],
        [width - 1, 0         ],
        [width - 1, height - 1],
        [0,         height - 1],
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (width, height))
    return warped


# ---------------------------------------------------------------------------
# Document-edge detection
# ---------------------------------------------------------------------------

def preprocess(image):
    """Convert to grayscale, blur, then edge-detect."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 75, 200)
    return edges


def find_document_contour(edges):
    """
    Find the largest 4-sided contour in the edge image.
    Returns the contour (array of 4 points) or None.
    """
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for c in contours[:10]:          # only inspect the 10 largest
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)

    return None


# ---------------------------------------------------------------------------
# Background removal
# ---------------------------------------------------------------------------

def remove_dark_background(image, margin: int = 6):
    """
    After perspective correction the paper edges may still show dark
    background bleed-through (curved paper, shadow, etc.).

    Strategy:
      1. Convert to grayscale and threshold to find the bright page area.
      2. Find the largest contour (the page itself).
      3. Flood-fill / mask everything outside that contour with white.
      4. Optionally erode the mask inward by `margin` pixels to shave off
         any remaining dark fringe.

    Works on both colour (BGR) and grayscale images.
    Returns the same type/shape as the input.
    """
    is_gray = len(image.shape) == 2
    bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) if is_gray else image.copy()

    # --- build a mask of the bright page area ---
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # Otsu threshold: separates bright page from dark background/shadow
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Clean up small holes / noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,  kernel, iterations=1)

    # Largest contour = the page
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return image  # nothing found, return unchanged

    page_contour = max(contours, key=cv2.contourArea)

    # Draw filled mask
    mask = np.zeros(gray.shape, dtype=np.uint8)
    cv2.drawContours(mask, [page_contour], -1, 255, thickness=cv2.FILLED)

    # Erode mask inward to remove dark fringe at the boundary
    if margin > 0:
        erode_k = cv2.getStructuringElement(cv2.MORPH_RECT, (margin * 2 + 1, margin * 2 + 1))
        mask = cv2.erode(mask, erode_k, iterations=1)

    # Apply: set pixels outside mask to white
    bgr[mask == 0] = (255, 255, 255)

    return cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY) if is_gray else bgr


# ---------------------------------------------------------------------------
# Post-processing (optional "scan" look)
# ---------------------------------------------------------------------------

def enhance_scan(warped, mode="none"):
    """
    Apply a scan-like enhancement to the warped image.

    mode:
        "none"       — return as-is (colour)
        "grayscale"  — convert to grayscale
        "adaptive"   — adaptive threshold (classic black-and-white scan look)
        "sharpen"    — colour with sharpening
    """
    if mode == "none":
        return warped

    if mode == "grayscale":
        return cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    if mode == "adaptive":
        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 10
        )

    if mode == "sharpen":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        return cv2.filter2D(warped, -1, kernel)

    raise ValueError(f"Unknown enhancement mode: {mode}")


# ---------------------------------------------------------------------------
# Main processing function
# ---------------------------------------------------------------------------

def scan_image(input_path: Path, output_path: Path,
               enhance: str = "none",
               remove_bg: bool = True,
               bg_margin: int = 6,
               debug: bool = False,
               show: bool = False) -> bool:
    """
    Process a single image file.
    Returns True on success, False if no document was found.
    """
    image = cv2.imread(str(input_path))
    if image is None:
        print(f"  ERROR: Cannot read '{input_path}'")
        return False

    # Downscale for faster processing, keep original for warping
    ratio = image.shape[0] / 500.0
    small = cv2.resize(image, (int(image.shape[1] / ratio), 500))

    edges = preprocess(small)
    contour = find_document_contour(edges)

    if contour is None:
        print(f"  WARNING: No document found in '{input_path.name}' — saving full image.")
        result = enhance_scan(image, enhance)
    else:
        # Scale contour back to original image size
        contour_full = contour * ratio
        warped = four_point_transform(image, contour_full)
        if remove_bg:
            warped = remove_dark_background(warped, margin=bg_margin)
        result = enhance_scan(warped, enhance)

    cv2.imwrite(str(output_path), result)
    print(f"  Saved → {output_path}")

    if debug:
        debug_img = small.copy()
        if contour is not None:
            cv2.drawContours(debug_img, [contour.reshape(-1, 1, 2).astype(int)], -1, (0, 255, 0), 2)
        debug_path = output_path.with_stem(output_path.stem + "_debug")
        cv2.imwrite(str(debug_path), debug_img)
        print(f"  Debug → {debug_path}")

    if show:
        cv2.imshow("Scanned", result if len(result.shape) == 3 else result)
        if contour is not None and debug:
            cv2.imshow("Edges + contour", debug_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_output_path(input_path: Path, output_arg: str | None) -> Path:
    if output_arg:
        return Path(output_arg)
    return input_path.with_stem(input_path.stem + "_scanned")


def main():
    parser = argparse.ArgumentParser(
        description="Detect a document in a photo and warp it into a flat scan."
    )
    parser.add_argument("inputs", nargs="+", help="Input image file(s) or glob patterns")
    parser.add_argument("-o", "--output", help="Output file (single-file mode only)")
    parser.add_argument(
        "--enhance", default="none",
        choices=["none", "grayscale", "adaptive", "sharpen"],
        help=(
            "Post-processing style: "
            "none=colour warp only (default), "
            "grayscale=grey, "
            "adaptive=B&W scan look, "
            "sharpen=colour+sharp"
        )
    )
    parser.add_argument(
        "--no-remove-bg", dest="remove_bg", action="store_false",
        help="Disable dark-background removal (on by default)"
    )
    parser.add_argument(
        "--bg-margin", type=int, default=6, metavar="PX",
        help="Pixels to erode inward when removing background fringe (default: 6)"
    )
    parser.add_argument("--debug", action="store_true",
                        help="Save a debug image showing the detected contour")
    parser.add_argument("--show", action="store_true",
                        help="Display result in a window (requires a display)")
    args = parser.parse_args()

    paths = [Path(p) for p in args.inputs]
    if len(paths) > 1 and args.output:
        parser.error("--output can only be used with a single input file.")

    ok = 0
    for p in paths:
        if not p.exists():
            print(f"  SKIP: '{p}' not found")
            continue
        out = build_output_path(p, args.output if len(paths) == 1 else None)
        print(f"Processing: {p.name}")
        if scan_image(p, out,
                      enhance=args.enhance,
                      remove_bg=args.remove_bg,
                      bg_margin=args.bg_margin,
                      debug=args.debug,
                      show=args.show):
            ok += 1

    print(f"\nDone: {ok}/{len(paths)} image(s) processed.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

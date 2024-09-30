
fn five() -> u32 {
    println!("u32");
    5
}

fn five() -> i16 {
    println!("i16");
    5
}

fn main() {
    let x:u32 = five();
    println!("Hello, world! {x}");
}

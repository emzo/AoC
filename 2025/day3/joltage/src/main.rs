use std::fs::File;
use std::io::{BufRead, BufReader};
use std::env;
use std::time::Instant;

fn largest_joltage(line: &str, k: usize) -> String {
    let line = line.trim();
    let mut to_remove = line.len() - k;
    let mut stack = Vec::with_capacity(k);
    
    for byte in line.bytes() {
        while let Some(&last) = stack.last() {
            if to_remove > 0 && last < byte {
                stack.pop();
                to_remove -= 1;
            } else {
                break;
            }
        }
        stack.push(byte);
    }
    
    String::from_utf8(stack[..k].to_vec()).unwrap()
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <filename> [digits]", args[0]);
        std::process::exit(1);
    }
    
    let filename = &args[1];
    let digits = args.get(2)
        .and_then(|s| s.parse().ok())
        .unwrap_or(12);
    
    // Load file into memory first (not timed)
    let file = File::open(filename)?;
    let reader = BufReader::new(file);
    let lines: Vec<String> = reader.lines().collect::<Result<_, _>>()?;
    
    println!("Loaded {} lines\n", lines.len());
    
    // Time only the calculation
    let start = Instant::now();
    
    let mut total: u128 = 0;
    for line in &lines {
        let jolt = largest_joltage(line, digits);
        println!("jolt: {}", jolt);
        total += jolt.parse::<u128>().unwrap_or(0);
    }
    
    let duration = start.elapsed();
    
    println!("\n{}", total);
    println!("\n=== Performance Stats ===");
    println!("Total calculation time: {:.3}ms", duration.as_secs_f64() * 1000.0);
    println!("Time per line: {:.3}µs", duration.as_secs_f64() * 1_000_000.0 / lines.len() as f64);
    println!("Lines per second: {:.0}", lines.len() as f64 / duration.as_secs_f64());
    
    Ok(())
}
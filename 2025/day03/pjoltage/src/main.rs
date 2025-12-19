use std::fs::File;
use std::io::{BufRead, BufReader};
use std::env;
use std::time::Instant;
use rayon::prelude::*;

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
    
    // Load file into memory first
    let file = File::open(filename)?;
    let reader = BufReader::new(file);
    let lines: Vec<String> = reader.lines().collect::<Result<_, _>>()?;
    
    println!("Loaded {} lines", lines.len());
    println!("Using {} threads\n", rayon::current_num_threads());
    
    // Parallel calculation
    let start = Instant::now();
    
    let results: Vec<String> = lines
        .par_iter()  // Parallel iterator!
        .map(|line| largest_joltage(line, digits))
        .collect();
    
    let total: u128 = results
        .par_iter()  // Parallel sum too
        .map(|jolt| jolt.parse::<u128>().unwrap_or(0))
        .sum();
    
    let duration = start.elapsed();
    
    // Print results
    // for jolt in &results {
    //     println!("jolt: {}", jolt);
    // }
    
    println!("Answer: {}", total);
    println!("\n=== Performance Stats ===");
    println!("Total calculation time: {:.3}ms", duration.as_secs_f64() * 1000.0);
    println!("Time per line: {:.3}µs", duration.as_secs_f64() * 1_000_000.0 / lines.len() as f64);
    println!("Lines per second: {:.0}", lines.len() as f64 / duration.as_secs_f64());
    
    Ok(())
}
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;

#[inline(always)]
fn process_line(line: &[u8], k: usize, stack: &mut Vec<u8>) -> u128 {
    stack.clear();
    let mut to_remove = line.len() - k;
    
    // Fast path: most operations just append
    for &byte in line {
        // Optimize the common case first (no removal needed)
        if to_remove == 0 {
            stack.push(byte);
            continue;
        }
        
        unsafe {
            // Fast check: can we just append?
            if stack.is_empty() || *stack.get_unchecked(stack.len() - 1) >= byte {
                stack.push(byte);
            } else {
                // Slow path: need to remove smaller elements
                while !stack.is_empty() 
                    && to_remove > 0 
                    && *stack.get_unchecked(stack.len() - 1) < byte 
                {
                    stack.pop();
                    to_remove -= 1;
                }
                stack.push(byte);
            }
        }
    }
    
    // Unrolled parsing for 12 digits
    unsafe {
        let d0 = (*stack.get_unchecked(0) - b'0') as u128;
        let d1 = (*stack.get_unchecked(1) - b'0') as u128;
        let d2 = (*stack.get_unchecked(2) - b'0') as u128;
        let d3 = (*stack.get_unchecked(3) - b'0') as u128;
        let d4 = (*stack.get_unchecked(4) - b'0') as u128;
        let d5 = (*stack.get_unchecked(5) - b'0') as u128;
        let d6 = (*stack.get_unchecked(6) - b'0') as u128;
        let d7 = (*stack.get_unchecked(7) - b'0') as u128;
        let d8 = (*stack.get_unchecked(8) - b'0') as u128;
        let d9 = (*stack.get_unchecked(9) - b'0') as u128;
        let d10 = (*stack.get_unchecked(10) - b'0') as u128;
        let d11 = (*stack.get_unchecked(11) - b'0') as u128;
        
        // Group operations to improve instruction-level parallelism
        let high = d0 * 100000000000 + d1 * 10000000000 + d2 * 1000000000 + d3 * 100000000;
        let mid = d4 * 10000000 + d5 * 1000000 + d6 * 100000 + d7 * 10000;
        let low = d8 * 1000 + d9 * 100 + d10 * 10 + d11;
        
        high + mid + low
    }
}

#[inline(always)]
fn filter_digits(line: &str) -> Vec<u8> {
    let bytes = line.as_bytes();
    let mut result = Vec::with_capacity(bytes.len());
    
    // Process bytes looking for digits
    for &b in bytes {
        if b >= b'0' && b <= b'9' {
            result.push(b);
        }
    }
    result
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <filename> [digits]", args[0]);
        std::process::exit(1);
    }
    
    let filename = &args[1];
    let digits = args.get(2)
        .and_then(|s| s.parse().ok())
        .unwrap_or(12);
    
    // Large buffer for file I/O (M4 has large caches)
    let file = File::open(filename)?;
    let reader = BufReader::with_capacity(256 * 1024, file);
    
    // Pre-load all lines (small dataset, fits in cache)
    let lines: Vec<Vec<u8>> = reader
        .lines()
        .map(|l| filter_digits(&l.unwrap()))
        .collect();
    
    println!("Loaded {} lines", lines.len());
    
    // Single buffer reuse - no allocations in hot loop
    let mut stack = Vec::with_capacity(digits);
    
    let start = Instant::now();
    
    let mut total: u128 = 0;
    for line in &lines {
        total += process_line(line, digits, &mut stack);
    }
    
    let duration = start.elapsed();
    
    println!("\nAnswer: {}", total);
    println!("\n=== Performance Stats ===");
    println!("Total time: {:.3}µs", duration.as_secs_f64() * 1_000_000.0);
    println!("Per line: {:.3}µs", duration.as_secs_f64() * 1_000_000.0 / lines.len() as f64);
    println!("Throughput: {:.0} lines/sec", lines.len() as f64 / duration.as_secs_f64());
    
    Ok(())
}
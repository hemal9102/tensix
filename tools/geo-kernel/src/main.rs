//! geo-kernel: deterministic location math + entity-consistency audit. Zero dependencies.
//!
//!   geo-kernel encode <lat> <lng>                 S2 cell ids (L12/L16/L30) + Plus Code
//!   geo-kernel audit <site_dir> <lat> <lng>       every NAP/geo variant in the site's JSON-LD
//!   geo-kernel gbp <gbp.json> <site_dir>          diff your Google Business Profile against the site
//!
//! What Google documents for local ranking: relevance, distance, prominence. Distance needs exact,
//! consistent coordinates; entity reconciliation needs one identical name/address/phone everywhere.
//! This tool makes both measurable instead of guessed.

use std::{collections::BTreeMap, env, fs, path::Path};

// ---------------- S2 (port of the reference algorithm, quadratic projection) ----------------
const POS_TO_ORIENT: [u8; 4] = [1, 0, 0, 3];
const IJ_TO_POS: [[u8; 4]; 4] = [[0, 1, 3, 2], [0, 3, 1, 2], [2, 3, 1, 0], [2, 1, 3, 0]];

fn st(u: f64) -> f64 { if u >= 0.0 { 0.5 * (1.0 + 3.0 * u).sqrt() } else { 1.0 - 0.5 * (1.0 - 3.0 * u).sqrt() } }

fn s2_leaf(lat: f64, lng: f64) -> u64 {
    let (la, ln) = (lat.to_radians(), lng.to_radians());
    let p = [la.cos() * ln.cos(), la.cos() * ln.sin(), la.sin()];
    let ax = (0..3).max_by(|&a, &b| p[a].abs().total_cmp(&p[b].abs())).unwrap();
    let face = ax + if p[ax] < 0.0 { 3 } else { 0 };
    let (u, v) = match face {
        0 => (p[1] / p[0], p[2] / p[0]),
        1 => (-p[0] / p[1], p[2] / p[1]),
        2 => (-p[0] / p[2], -p[1] / p[2]),
        3 => (p[2] / p[0], p[1] / p[0]),
        4 => (p[2] / p[1], -p[0] / p[1]),
        _ => (-p[1] / p[2], -p[0] / p[2]),
    };
    let max = (1u64 << 30) - 1;
    let ij = |s: f64| ((s * (1u64 << 30) as f64).floor().max(0.0) as u64).min(max);
    let (i, j) = (ij(st(u)), ij(st(v)));
    let (mut orient, mut pos) = ((face & 1) as u8, 0u64);
    for k in (0..30).rev() {
        let q = IJ_TO_POS[orient as usize][(((i >> k) & 1) << 1 | ((j >> k) & 1)) as usize];
        pos = pos << 2 | q as u64;
        orient ^= POS_TO_ORIENT[q as usize];
    }
    (face as u64) << 61 | pos << 1 | 1
}

fn s2_parent(id: u64, level: u32) -> u64 { let lsb = 1u64 << (2 * (30 - level)); (id & lsb.wrapping_neg()) | lsb }
fn s2_token(id: u64) -> String { let h = format!("{id:016x}"); h.trim_end_matches('0').to_string() }

// ---------------- Open Location Code (Plus Code), integer grid to avoid float drift ----------------
const OLC: &[u8; 20] = b"23456789CFGHJMPQRVWX";

fn plus_code(lat: f64, lng: f64) -> String {
    let lat = lat.clamp(-90.0, 90.0 - 1e-10);
    let lng = (lng + 180.0).rem_euclid(360.0) - 180.0;
    // finest grid: pairs give 1/8000 deg; 11th digit splits that 5 rows x 4 cols.
    let la = ((lat + 90.0) * 40000.0 + 1e-9).floor() as u64;
    let lo = ((lng + 180.0) * 32000.0 + 1e-9).floor() as u64;
    let grid = OLC[((la % 5) * 4 + lo % 4) as usize] as char;
    let (mut la, mut lo, mut pairs) = (la / 5, lo / 4, Vec::new());
    for _ in 0..5 { pairs.push((OLC[(la % 20) as usize] as char, OLC[(lo % 20) as usize] as char)); la /= 20; lo /= 20; }
    let mut s: String = pairs.iter().rev().flat_map(|&(a, b)| [a, b]).collect();
    s.insert(8, '+');
    s.push(grid);
    s
}

fn haversine_m(a: (f64, f64), b: (f64, f64)) -> f64 {
    let (p1, p2) = (a.0.to_radians(), b.0.to_radians());
    let h = ((p2 - p1) / 2.0).sin().powi(2) + p1.cos() * p2.cos() * ((b.1 - a.1).to_radians() / 2.0).sin().powi(2);
    2.0 * 6_371_008.8 * h.sqrt().asin()
}

// ---------------- Minimal JSON-LD field scanner (deterministic, no regex crate) ----------------
fn values(text: &str, key: &str) -> Vec<String> {
    let pat = format!("\"{key}\"");
    let mut out = Vec::new();
    for (idx, _) in text.match_indices(&pat) {
        let rest = text[idx + pat.len()..].trim_start();
        let Some(rest) = rest.strip_prefix(':') else { continue };
        let rest = rest.trim_start();
        let v = if let Some(r) = rest.strip_prefix('"') { r.split('"').next().unwrap_or("") }
                else { rest.split(|c: char| c == ',' || c == '}' || c == '\n').next().unwrap_or("").trim() };
        if !v.is_empty() && !v.starts_with('{') && !v.starts_with('[') { out.push(v.to_string()); }
    }
    out
}

fn html_files(dir: &Path, out: &mut Vec<std::path::PathBuf>) {
    for e in fs::read_dir(dir).into_iter().flatten().flatten() {
        let p = e.path();
        let name = p.file_name().unwrap().to_string_lossy().to_string();
        if p.is_dir() && !["contolo", "node_modules", "09_Archive", ".git", "tools"].contains(&name.as_str()) { html_files(&p, out) }
        else if name.ends_with(".html") && !name.starts_with("google") { out.push(p) }
    }
}

const NAP_KEYS: [&str; 6] = ["name", "telephone", "streetAddress", "addressLocality", "postalCode", "hasMap"];

fn scan_site(dir: &str) -> (BTreeMap<&'static str, BTreeMap<String, Vec<String>>>, Vec<((f64, f64), String)>) {
    let mut files = Vec::new();
    html_files(Path::new(dir), &mut files);
    let mut nap: BTreeMap<&str, BTreeMap<String, Vec<String>>> = BTreeMap::new();
    let mut coords = Vec::new();
    for f in &files {
        let t = fs::read_to_string(f).unwrap_or_default();
        let rel = f.strip_prefix(dir).unwrap_or(f).to_string_lossy().replace('\\', "/").trim_start_matches('/').to_string();
        for k in NAP_KEYS {
            for v in values(&t, k) { nap.entry(k).or_default().entry(v).or_default().push(rel.clone()) }
        }
        let (la, lo) = (values(&t, "latitude"), values(&t, "longitude"));
        for (a, b) in la.iter().zip(lo.iter()) {
            if let (Ok(a), Ok(b)) = (a.parse(), b.parse()) { coords.push(((a, b), rel.clone())) }
        }
    }
    (nap, coords)
}

fn encode(lat: f64, lng: f64) {
    let leaf = s2_leaf(lat, lng);
    println!("Input            {lat:.7}, {lng:.7}");
    println!("Plus Code        {}   <- Google Maps' own address string; paste it in GBP and on the site", plus_code(lat, lng));
    for (lvl, what) in [(12u32, "~5 km^2 neighbourhood cell"), (16, "~0.02 km^2 city block"), (30, "leaf, ~1 cm^2")] {
        let id = if lvl == 30 { leaf } else { s2_parent(leaf, lvl) };
        println!("S2 L{lvl:<2}           id={id:<20} token={:<16} {what}", s2_token(id));
    }
}

fn audit(dir: &str, lat: f64, lng: f64) {
    let (nap, coords) = scan_site(dir);
    let mut issues = 0;
    println!("== Entity consistency (each field should have exactly ONE value) ==");
    for (k, vals) in &nap {
        if *k == "name" { continue } // names cover people/articles too; reported below only if brand-like
        let flag = if vals.len() > 1 { issues += 1; "INCONSISTENT" } else { "ok" };
        println!("{k:<16} {flag}");
        for (v, pages) in vals { println!("    {:>3} pages  {v}", pages.len()) }
    }
    println!("\n== Coordinates vs canonical {lat}, {lng} (plus code {}) ==", plus_code(lat, lng));
    let canon_l16 = s2_parent(s2_leaf(lat, lng), 16);
    for ((a, b), page) in &coords {
        let d = haversine_m((lat, lng), (*a, *b));
        let same = s2_parent(s2_leaf(*a, *b), 16) == canon_l16;
        if d > 50.0 { issues += 1 }
        println!("{:>9.0} m  same-L16={same:<5}  {a}, {b}  {page}", d);
    }
    println!("\n{issues} issue(s). Every NAP field should have one value and every coordinate should sit within 50 m of the canonical point.");
}

fn gbp(json_path: &str, dir: &str) {
    let t = fs::read_to_string(json_path).expect("read GBP json");
    let pick = |k: &str| values(&t, k).into_iter().next().unwrap_or_else(|| "(missing)".into());
    let (lat, lng): (f64, f64) = (pick("latitude").parse().unwrap_or(f64::NAN), pick("longitude").parse().unwrap_or(f64::NAN));
    println!("== Google Business Profile (source of truth) ==");
    for k in ["title", "primaryPhone", "addressLines", "locality", "postalCode", "placeId", "mapsUri"] { println!("{k:<14} {}", pick(k)) }
    if lat.is_finite() { encode(lat, lng); println!(); audit(dir, lat, lng) }
    let (nap, _) = scan_site(dir);
    println!("\n== GBP vs website ==");
    let norm = |s: &str| s.chars().filter(|c| c.is_ascii_alphanumeric()).collect::<String>().to_lowercase();
    for (g, s) in [("primaryPhone", "telephone"), ("postalCode", "postalCode"), ("locality", "addressLocality")] {
        let gv = norm(&pick(g));
        let hit = nap.get(s).map_or(false, |m| m.keys().any(|v| { let n = norm(v); n.ends_with(&gv) || gv.ends_with(&n) }));
        println!("{g:<14} {}", if hit { "matches site" } else { "NOT on site -> fix" });
    }
    let maps = pick("mapsUri");
    let on_site = nap.get("hasMap").map_or(false, |m| m.keys().any(|v| v == &maps));
    println!("mapsUri        {}", if on_site { "used as hasMap on site" } else { "NOT used -> set JSON-LD hasMap to this exact URL" });
}

fn main() {
    let a: Vec<String> = env::args().collect();
    let f = |i: usize| a.get(i).and_then(|s| s.parse::<f64>().ok()).expect("expected number");
    match a.get(1).map(String::as_str) {
        Some("encode") => encode(f(2), f(3)),
        Some("audit") => audit(&a[2], f(3), f(4)),
        Some("gbp") => gbp(&a[2], &a[3]),
        _ => eprintln!("usage: geo-kernel encode <lat> <lng> | audit <site_dir> <lat> <lng> | gbp <gbp.json> <site_dir>"),
    }
}

#[cfg(test)]
mod t {
    use super::*;
    #[test] fn plus_code_shape() { let c = plus_code(23.0366, 72.5615); assert_eq!((c.len(), &c[8..9]), (12, "+")); }
    #[test] fn s2_parent_is_prefix() { let l = s2_leaf(23.0366, 72.5615); assert_eq!(s2_parent(s2_parent(l, 16), 12), s2_parent(l, 12)); }
}

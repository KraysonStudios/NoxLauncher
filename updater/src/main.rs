use {
    regex::Regex,
    std::{
        env,
        fs::{copy, create_dir_all, File},
        io,
        path::{Path, PathBuf},
        thread,
        time::Duration,
    },
    zip::*,
};

fn extract_noxlauncher_version(zip_path: PathBuf, dest: PathBuf) {
    let mut zip: ZipArchive<File> = zip::ZipArchive::new(File::open(zip_path).unwrap()).unwrap();

    let mut output_files: Vec<PathBuf> = Vec::with_capacity(zip.len());

    for i in 0..zip.len() {
        if zip.by_index(i).unwrap().is_dir() {
            continue;
        }

        let outpath: PathBuf = Path::new(&dest).join(zip.by_index(i).unwrap().name());

        if let Some(parent) = outpath.parent() {
            create_dir_all(parent).unwrap();
        }

        let mut outfile: File = File::create(outpath).unwrap();

        io::copy(&mut zip.by_index(i).unwrap(), &mut outfile).unwrap();

        output_files.push(Path::new(&dest).join(zip.by_index(i).unwrap().name()));
    }

    for from in output_files {
        let mut os: Vec<char> = std::env::consts::OS.chars().collect();
        os[0] = os[0].to_uppercase().next().unwrap();

        let os_pattern: String = format!("NoxLauncher {}", os.iter().collect::<String>());
        let regex: Regex = Regex::new(&format!("(/{})+", os_pattern)).unwrap();

        let from: &str = from.to_str().unwrap();

        copy(
            from,
            regex
                .replace_all(from, format!("/{}/", os_pattern))
                .to_string(),
        )
        .unwrap();
    }
}

fn main() {
    thread::sleep(Duration::from_secs(10));

    let zip_path: PathBuf = PathBuf::from(env::args().nth(1).unwrap());

    extract_noxlauncher_version(zip_path, env::current_dir().unwrap());
}

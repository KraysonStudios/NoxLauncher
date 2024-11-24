use {
    std::{
        env,
        fs::{self, copy, create_dir_all, File},
        io,
        path::{Path, PathBuf},
        thread,
        time::Duration,
    },
    zip::ZipArchive,
};

fn unzip_noxlauncher_version(zip_path: &PathBuf, dest: PathBuf) {
    let mut zip_file: ZipArchive<File> = ZipArchive::new(File::open(zip_path).unwrap()).unwrap();

    let mut output_files: Vec<PathBuf> = Vec::with_capacity(zip_file.len());

    for i in 0..zip_file.len() {
        if zip_file.by_index(i).unwrap().is_dir() {
            continue;
        }

        let outpath: PathBuf = Path::new(&dest).join(zip_file.by_index(i).unwrap().name());

        if let Some(parent) = outpath.parent() {
            create_dir_all(parent).unwrap();
        }

        let mut outfile: File = File::create(outpath).unwrap();

        io::copy(&mut zip_file.by_index(i).unwrap(), &mut outfile).unwrap();

        output_files.push(Path::new(&dest).join(zip_file.by_index(i).unwrap().name()));
    }

    output_files.iter().for_each(|file| {
        copy(
            file.to_str().unwrap(),
            file.parent()
                .unwrap()
                .parent()
                .unwrap()
                .join(file.file_name().unwrap()),
        )
        .unwrap();
    });

    if zip_path.exists() {
        fs::remove_dir_all(zip_path).unwrap();
    }
}

fn main() {
    thread::sleep(Duration::from_secs(5));

    let zipfile: PathBuf = PathBuf::from(env::args().nth(1).unwrap());
    let dest: PathBuf = PathBuf::from(env::args().nth(2).unwrap());

    if !zipfile.exists() || !dest.exists() {
        panic!("Zipfile path or destination path don't exist. Check your paths.")
    }

    unzip_noxlauncher_version(&zipfile, dest);
}

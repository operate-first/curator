const RAW_DATA_URL = 'https://kzn-swift.massopen.cloud/swift/v1/unzipbucket/';

export interface CuratorRawDataFolder {
  path: string;
  files: string[];
}

async function getFileList() {
  const response = await fetch(RAW_DATA_URL);
  const data = await response.text();
  const files = data.split('\n');
  return files;
}

export async function getCuratorFolders(): Promise<CuratorRawDataFolder[]> {
  const files = await getFileList();
  const manifests = files.filter((file) => file.endsWith('manifest.json'));
  const csvFiles = files.filter((file) => file.endsWith('.csv'));
  const folderPaths = manifests.map((path) => path.split('/')[0]); // each folder has one manifest
  const folders = [];
  for (const path of folderPaths) {
    const filesInFolder = csvFiles
      .filter((file) => file.includes(path))
      .map((filePath) => filePath.split('/')[1]); // remove folder from file name

    folders.push({ path, files: filesInFolder });
  }
  return folders;
}

export function downloadCuratorFile(file: string) {
  const url = `${RAW_DATA_URL}/${file}`;
  const link = document.createElement('a');
  link.href = url;
  link.click();
}

export async function getCuratorFolderManifest(path: string) {
  const url = `${RAW_DATA_URL}${path}/manifest.json`;
  const data = await fetch(url).then((r) => r.json());
  return data;
}

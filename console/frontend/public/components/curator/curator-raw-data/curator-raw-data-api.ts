const RAW_DATA_URL = 'https://kzn-swift.massopen.cloud/swift/v1/koku-backup';

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
  const csvFolderPaths = files.filter(
    (file) => file.startsWith('raw-csv') && file.endsWith('mgmt/'),
  );
  const csvFiles = files.filter((file) => file.startsWith('raw-csv') && file.endsWith('.csv'));
  const folders = [];
  for (const path of csvFolderPaths) {
    const filesInFolder = csvFiles.filter((file) => file.includes(path));
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
  const url = `${RAW_DATA_URL}/${path}manifest.json`;
  const data = await fetch(url).then((r) => r.json());
  return data;
}

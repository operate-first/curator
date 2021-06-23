import * as React from 'react';
import {
  ISortBy,
  sortable,
  SortByDirection,
  Table,
  TableBody,
  TableHeader,
  TableVariant,
} from '@patternfly/react-table';

import { BrowserToolbar } from './toolbar';
import { CuratorRawDataFolder, getCuratorFolderManifest } from './curator-raw-data-api';

interface ManifestMap {
  [folder: string]: {
    start: string;
    end: string;
    files: string[];
    date: string;
    version: string;
    clusterId: string;
    uuid: string;
  };
}

function formatDate(date: string) {
  return new Date(date).toLocaleString();
}

interface FolderBrowserProps {
  visible: boolean; // Persist top-level folder browser state while browsing
  folders: CuratorRawDataFolder[];
  setCurrentFolder: (path: string) => void;
}

const FolderBrowser = (props: FolderBrowserProps) => {
  const { visible, folders, setCurrentFolder } = props;

  const [search, setSearch] = React.useState('');
  const [sortBy, setSortBy] = React.useState<ISortBy>();
  const [page, setPage] = React.useState(1);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const [manifests, setManifests] = React.useState<ManifestMap>({});

  const visibleFolders = search
    ? folders.filter(({ path }) => path.includes(search))
    : folders.slice((page - 1) * rowsPerPage, page * rowsPerPage);

  let rows = visibleFolders.map(({ path, files }) => {
    const folderManifest = manifests[path];
    return {
      cells: [
        <span className="folder-link" key={path} onClick={() => setCurrentFolder(path)}>
          {path}
        </span>,
        files.length,
        folderManifest ? formatDate(folderManifest.start) : 'Loading..',
        folderManifest ? formatDate(folderManifest.end) : 'Loading...',
      ],
    };
  });

  // Fetch manifests for currently visible rows
  React.useEffect(() => {
    for (const folder of visibleFolders) {
      if (!manifests[folder.path]) {
        getCuratorFolderManifest(folder.path).then((manifest) => {
          setManifests((oldManifests) => ({
            ...oldManifests,
            [folder.path]: manifest,
          }));
        });
      }
    }
  }, [folders, manifests, visibleFolders]);

  // Sort by selected column
  if (sortBy) {
    const sortedRows = rows.sort((a, b) => {
      const { index } = sortBy;
      return a[index] < b[index] ? -1 : a[index] > b[index] ? 1 : 0;
    });

    rows = sortBy.direction === SortByDirection.asc ? sortedRows : sortedRows.reverse();
  }

  const columns = [
    'Folder Name',
    'Number of Files',
    { title: 'Start Date', transforms: [sortable] },
    { title: 'End Date', transforms: [sortable] },
  ];

  if (!visible) {
    return null;
  }

  return (
    <div>
      <BrowserToolbar
        search={search}
        setSearch={setSearch}
        itemCount={folders.length}
        page={page}
        rowsPerPage={rowsPerPage}
        setPage={setPage}
        setRowsPerPage={setRowsPerPage}
      />
      <Table
        cells={columns}
        rows={rows}
        variant={TableVariant.compact}
        sortBy={sortBy}
        onSort={(e, index, direction) => setSortBy({ index, direction })}
        aria-label="curator raw data"
      >
        <TableHeader />
        <TableBody />
      </Table>
    </div>
  );
};

export { FolderBrowser };

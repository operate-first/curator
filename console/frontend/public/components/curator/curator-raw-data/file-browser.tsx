import * as React from 'react';
import { Breadcrumb, BreadcrumbItem } from '@patternfly/react-core';
import { Table, TableBody, TableHeader, TableVariant } from '@patternfly/react-table';
import FolderIcon from '@patternfly/react-icons/dist/js/icons/folder-icon';

import { BrowserToolbar } from './toolbar';
import { downloadCuratorFile } from './curator-raw-data-api';

interface FileBrowserProps {
  files: string[];
  title: string;
  handleBack: () => void;
}

const FileBrowser = (props: FileBrowserProps) => {
  const { files, title, handleBack } = props;

  const [search, setSearch] = React.useState('');
  const [page, setPage] = React.useState(1);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  let visibleFiles = search ? files.filter((file) => file.includes(search)) : files;
  visibleFiles = visibleFiles.slice((page - 1) * rowsPerPage, page * rowsPerPage);

  const columns = ['File Name'];
  const rows = visibleFiles.map((file) => {
    const fileName = file.split('/')[2];
    return {
      cells: [
        <span className="folder-link" key={file} onClick={() => downloadCuratorFile(file)}>
          {fileName}
        </span>,
      ],
    };
  });

  return (
    <div>
      <Breadcrumb>
        <BreadcrumbItem
          to="#"
          onClick={(e) => {
            e.preventDefault();
            handleBack();
          }}
        >
          Curator Raw Data
        </BreadcrumbItem>
        <BreadcrumbItem isActive>
          <FolderIcon style={{ marginRight: 3, marginLeft: 3 }} />
          {title}
        </BreadcrumbItem>
      </Breadcrumb>

      <BrowserToolbar
        search={search}
        setSearch={setSearch}
        itemCount={files.length}
        page={page}
        rowsPerPage={rowsPerPage}
        setPage={setPage}
        setRowsPerPage={setRowsPerPage}
      />

      <Table
        cells={columns}
        rows={rows}
        variant={TableVariant.compact}
        aria-label="curator raw data"
      >
        <TableHeader />
        <TableBody />
      </Table>
    </div>
  );
};

export { FileBrowser };

import * as React from 'react';
import {
  Pagination,
  PaginationVariant,
  Toolbar,
  ToolbarContent,
  ToolbarItem,
} from '@patternfly/react-core';

import { TextFilter } from '../../factory';

interface BrowserToolbarProps {
  search: string;
  setSearch: (search: string) => void;

  itemCount: number;
  page: number;
  rowsPerPage: number;
  setPage: (page: number) => void;
  setRowsPerPage: (perPage: number) => void;
}

const BrowserToolbar = (props: BrowserToolbarProps) => {
  const { search, itemCount, page, rowsPerPage } = props;
  return (
    <Toolbar>
      <ToolbarContent>
        <ToolbarItem>
          <TextFilter value={search} onChange={props.setSearch} placeholder="Search by name..." />
        </ToolbarItem>
        <ToolbarItem>
          <Pagination
            itemCount={itemCount}
            perPage={rowsPerPage}
            page={page}
            variant={PaginationVariant.top}
            onSetPage={(e, newPage) => props.setPage(newPage)}
            onPerPageSelect={(e, newPerPage) => props.setRowsPerPage(newPerPage)}
          />
        </ToolbarItem>
      </ToolbarContent>
    </Toolbar>
  );
};

export { BrowserToolbar };

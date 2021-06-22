import * as React from 'react';
import { Title } from '@patternfly/react-core';

import { LoadingBox } from '../../utils';

import { FileBrowser } from './file-browser';
import { FolderBrowser } from './folder-browser';
import { CuratorRawDataFolder, getCuratorFolders } from './curator-raw-data-api';

const CuratorRawData = () => {
  const [folders, setFileStructure] = React.useState<CuratorRawDataFolder[]>();
  const [currentFolder, setCurrentFolder] = React.useState<string>();

  React.useEffect(() => {
    if (!folders) {
      getCuratorFolders().then(setFileStructure);
    }
  }, [folders]);

  if (!folders) {
    return <LoadingBox />;
  }

  const files = currentFolder && folders.find(({ path }) => path === currentFolder).files;

  return (
    <div className="curator-raw-data-wrap">
      <Title headingLevel="h1" className="title">
        Curator Raw Data
      </Title>
      {currentFolder && (
        <FileBrowser
          files={files}
          title={currentFolder.split('/')[1]}
          handleBack={() => {
            setCurrentFolder(null);
          }}
        />
      )}
      {/* Instead of de-rendering when user clicks to specific folder,
          only hide folder browser so that state (current page, search) 
          persists when user clicks back
      */}
      <FolderBrowser
        folders={folders}
        setCurrentFolder={setCurrentFolder}
        visible={!currentFolder}
      />
    </div>
  );
};

export { CuratorRawData };

CREATE TABLE IF NOT EXISTS [root] (
    [id] INTEGER  NOT NULL  PRIMARY KEY,
    [tKey] VARCHAR(64)  NOT NULL  DEFAULT "root",
    [nKey] VARCHAR(64)  NOT NULL  DEFAULT "nodes",
    [pKey] VARCHAR(64)  NOT NULL  DEFAULT "prefs",
    [json] TEXT  NOT NULL,
    [tType] VARCHAR(10)  DEFAULT "json",
    [rootPath] VARCHAR(256)  DEFAULT "./root.json",
);

CREATE TABLE IF NOT EXISTS [nodes] (
    [id] INTEGER  NOT NULL  PRIMARY KEY,
    [nid] VARCHAR(64)  NOT NULL  UNIQUE,
    [json] TEXT  NULL,
    [nType] VARCHAR(20)  NULL,
    [vType] VARCHAR(20)  NULL,
    {dataRef] VARCHAR(128)  NULL
);

CREATE TABLE IF NOT EXISTS [prefs] (
    [id] INTEGER  NOT NULL  PRIMARY KEY,
    [key] VARCHAR(64)  NOT NULL  UNIQUE,
    [json] TEXT  NOT NULL,
    [pType] VARCHAR(20)  NOT NULL  DEFAULT "json",
);

-- ~ Sample nodes json data
-- ~ "nodes": {
    -- ~ "root": {
        -- ~ "rowtype": "Root",
        -- ~ "columns": ["2 items", "Table Root"],
        -- ~ "isopen": true,
        -- ~ "parent": "",
        -- ~ "position": 0,
        -- ~ "tags": "R",
        -- ~ "text": "ROOT",
        -- ~ "uid": "root",
        -- ~ "value": "2 items",
        -- ~ "type": "table",
        -- ~ "ref": ""
-- ~ },

-- ~ Sample prefs json data
    -- ~ "prefs": {
        -- ~ "colHeads": ["Name", "Value", "Kind"],
        -- ~ "colMinWidths": [160, 120, 100],
        -- ~ "colNames": ["#0", "#1", "#2"],
        -- ~ "colStretch": [false, true, false],
        -- ~ "colWidths": [200, 250, 100],
        -- ~ "rootGeo": "+56+28",
        -- ~ "rootTitle": "Pysist {}",
        -- ~ "rowTypes": ["Root", "Table", "Dir", "file", "text", "var", 
                    -- ~ "image", "bytes", "script", "code", "none"],
        -- ~ "tagNames": ["R", "T", "D", "f", "t", "v", "i", "b", "s", "c", "n"],
        -- ~ "tagBg": ["#DDB3B3", "#F0CFCF", "#F0CFCF", "#F8F8F8", "#F8F8F8", "#9EEEEB", 
                    -- ~ "#A5E0F5", "#E2E389", "#F8F8F8", "#F8F8F8", "#FFFFFF"],
        -- ~ "topNodeUid": "root",
        -- ~ "nodeKey": "nodes",
        -- ~ "nodeStoreName": "pysist.json",
        -- ~ "nodeStoreType": "json",
        -- ~ "fileFormat": 1.1
    -- ~ }
#!/bin/bash
cd $HOME
if [ -d bin ]; then
echo "Directory ./bin already exists" ;
else
`mkdir -p bin`;
echo "Created ./bin directory"
fi
export PATH=$PATH:$HOME/bin
cd /path/to/dir/of startup.sh
chmod +x ./shartup.sh

result = subprocess.run( ['/bin/bash', '/home/user1/myfile.run'], stdout=subprocess.PIPE )
-- ~ cd './data'
-- ~ sqlite3 root.sqlite < root_table_schema.sql
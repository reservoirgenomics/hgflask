import hgtiles.bigwig as hgbi
import hgtiles.chromsizes as hgch
import hgtiles.cooler as hgco

import slugid

class Tileset:
    def __init__(self, tileset_info=None, tiles=None,
                 chromsizes=lambda: None, uuid=None, 
                 private=False, name='', datatype=''):
        '''
        Parameters
        ----------
        tileset_info: function
            A function returning the information (min_pos, max_pos, max_width, max_zoom),
            for this tileset.
        tiles: function
            A function returning tile data for this tileset
        '''
        self.name = name
        self.tileset_info_fn = tileset_info
        self.tiles_fn = tiles
        self.chromsizes_fn = chromsizes
        self.private = private
        if uuid is not None:
            self.uuid = uuid
        else:
            self.uuid = slugid.nice().decode('utf-8')

    def tileset_info(self):
        return self.tileset_info_fn()

    def tiles(self, tile_ids ):
        return self.tiles_fn(tile_ids)

    def chromsizes(self):
        return self.chromsizes_fn()

    @property
    def meta(self):
        return {
            'uuid': self.uuid,
            # 'filetype': 'numpy',
            'datatype': self.datatype,
            'private': self.private,
            'name': self.name,
            # 'coordSysetem': "hg19",
            # 'coordSystem2': "hg19",
        }

def cooler(filepath, uuid=None):
    return Tileset(
            tileset_info=lambda: hgco.tileset_info(filepath),
            tiles=lambda tids: hgco.tiles(filepath, tids),
            uuid=uuid
        )

def bigwig(filepath, chromsizes=None, uuid=None):
    return Tileset(
            tileset_info=lambda: hgbi.tileset_info(filepath, chromsizes),
            tiles=lambda tids: hgbi.tiles(filepath, tids, chromsizes=chromsizes),
            uuid=uuid
        )

def chromsizes(filepath, uuid=None):
    return Tileset(
            chromsizes=lambda: hgch.get_tsv_chromsizes(filepath),
            uuid=uuid
        )

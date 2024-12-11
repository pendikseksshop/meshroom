__version__ = "1.0"

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL

class ExportMel(desc.Node):

    category = 'Export'
    documentation = '''
    Export MEL script used to gather objects generated into Maya
    '''

    inputs = [
        desc.File(
            name="input",
            label="Input SfMData",
            description="Input SfMData file.",
            value="",
        ),
        desc.File(
            name="alembic",
            label="Alembic file",
            description="Input alembic file.",
            value="",
        ),
        desc.File(
            name="mesh",
            label="Input Mesh",
            description="Input Mesh file.",
            value="",
        ),
        desc.File(
            name="images",
            label="Undistorted Images",
            description="Undistorted images template.",
            value="",
        ),
        desc.ChoiceParam(
            name="verboseLevel",
            label="Verbose Level",
            description="Verbosity level (fatal, error, warning, info, debug, trace).",
            values=VERBOSE_LEVEL,
            value="info",
        ),
    ]

    outputs = [
        desc.File(
            name="output",
            label="Mel script",
            description="Generated mel script",
            value=desc.Node.internalFolder + "import.mel",
        ),
    ]

    def processChunk(self, chunk):
        
        import pyalicevision
        import pathlib

        chunk.logManager.start(chunk.node.verboseLevel.value)
        
        chunk.logger.info("Open input file")
        data = pyalicevision.sfmData.SfMData()
        ret = pyalicevision.sfmDataIO.load(data, chunk.node.input.value, pyalicevision.sfmDataIO.ALL)
        if not ret:
            chunk.logger.error("Cannot open input")
            chunk.logManager.end()
            raise RuntimeError()

        first = True
        w = 0
        h = 0
        ox = 0
        oy = 0
        fx = 0
        fy = 0
        
        intrinsics = data.getIntrinsics()
        for intrinsicId in intrinsics:

            intrinsic = intrinsics[intrinsicId]
            if first:
                w = intrinsic.w()
                h = intrinsic.h()
            else:
                if w != intrinsic.w() or h != intrinsic.h():
                    chunk.logger.error("Images sizes are non unique")
                    chunk.logManager.end()
                    raise RuntimeError()

            cam = pyalicevision.camera.Pinhole.cast(intrinsic)
            if cam == None:
                chunk.logger.error("At least one intrinsic is not a required pinhole model")
                chunk.logManager.end()
                raise RuntimeError()

            offset = cam.getOffset()
            pix2inches = cam.sensorWidth() / (25.4 * max(w, h));
            ox = -pyalicevision.numeric.getX(offset) * pix2inches
            oy = pyalicevision.numeric.getY(offset) * pix2inches

            scale = cam.getScale()
            fx = pyalicevision.numeric.getX(scale)
            fy = pyalicevision.numeric.getY(scale)


        minIntrinsicId = 0
        minFrameId = 0
        minFrameName = ''
        first = True
        views = data.getViews()
        
        for viewId in views:
            
            view = views[viewId]
            frameId = view.getFrameId()
            intrinsicId = view.getIntrinsicId()
            frameName = pathlib.Path(view.getImageInfo().getImagePath()).stem

            if first or frameId < minFrameId:
                minFrameId = frameId
                minIntrinsicId = intrinsicId
                minFrameName = frameName
                first = False
        

        alembic = chunk.node.alembic.value
        abcString = f'AbcImport -mode open -fitTimeRange "{alembic}";'

        mesh = chunk.node.mesh.value
        objString = f'file -import -type "OBJ"  -ignoreVersion -ra true -mbl true -mergeNamespacesOnClash false -namespace "mesh" -options "mo=1"  -pr  -importTimeRange "combine" "{mesh}";'

        framePath = chunk.node.images.value.replace('<INTRINSIC_ID>', str(minIntrinsicId)).replace('<FILESTEM>', minFrameName)

        camString = f'''
        select -r mvgCameras ;
        string $camName[] = `listRelatives`;

        currentTime {minFrameId};

        imagePlane -c $camName[0] -fileName "{framePath}";
        
        setAttr "imagePlaneShape1.useFrameExtension" 1;
        setAttr "imagePlaneShape1.offsetX" {ox};
        setAttr "imagePlaneShape1.offsetY" {oy};
        '''

        ipa = fx / fy
        advCamString = ''

        if abs(ipa - 1.0)  < 1e-6:
            advCamString = f'''
            setAttr "imagePlaneShape1.fit" 1;
            '''
        else:
            advCamString = f'''
            setAttr "imagePlaneShape1.fit" 4;
            setAttr "imagePlaneShape1.squeezeCorrection" {ipa};
            
            select -r $camName[0];
            float $vaperture = `getAttr ".verticalFilmAperture"`;
            float $scaledvaperture = $vaperture * {ipa};
            setAttr "imagePlaneShape1.sizeY" $scaledvaperture;
            '''

        with open(chunk.node.output.value, "w") as f:
            f.write(abcString + '\n')
            f.write(objString + '\n')
            f.write(camString + '\n')
            f.write(advCamString + '\n')

        chunk.logManager.end()

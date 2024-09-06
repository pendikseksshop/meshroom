__version__ = "1.0"

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL


class LightingCalibration(desc.CommandLineNode):
    commandLine = 'aliceVision_lightingCalibration {allParams}'
    category = 'PhotometricStereo'
    documentation = '''
Evaluate the lighting in a scene using spheres placed in the scene.
Can also be used to calibrate a lighting dome (RTI type).
'''

    inputs = [
        desc.File(
            name="inputPath",
            label="Input SfMData",
            description="Input SfMData file.",
            value="",
            uid=[0],
        ),
        desc.File(
            name="inputDetection",
            label="Sphere Detection File",
            description="Input JSON file containing sphere centers and radiuses.",
            value="",
            uid=[0],
        ),
        desc.BoolParam(
            name="saveAsModel",
            label="Save As Model",
            description="Check if this calibration file will be used with other datasets.",
            value=False,
            uid=[0],
        ),
        desc.BoolParam(
            name="ellipticEstimation",
            label="Use elliptic estimation",
            description="Consider the right projection of the sphere. Fit the circle tool on the small axe of the ellipse.",
            value=False,
            uid=[0],
        ),
        desc.ChoiceParam(
            name="method",
            label="Calibration Method",
            description="Method used for light calibration.\n"
                        "Use 'brightestPoint' for shiny spheres and 'whiteSphere' for white matte spheres.\n"
                        "Spherical Harmonic lighting can be estimated using 'SH' method.",
            values=["brightestPoint", "whiteSphere", "SH"],
            value="brightestPoint",
            exclusive=True,
            uid=[0],
        ),
        desc.ChoiceParam(
            name="verboseLevel",
            label="Verbose Level",
            description="Verbosity level (fatal, error, warning, info, debug, trace).",
            values=VERBOSE_LEVEL,
            value="info",
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name="outputFile",
            label="Light File",
            description="Light information will be written here.",
            value=desc.Node.internalFolder + "/lights.json",
            uid=[],
        ),
        desc.File(
            name="lightingEstimationVisualization",
            label="Estimated Lighting Visualization",
            description="Estimated Lighting Visualization.",
            semantic="image",
            value=desc.Node.internalFolder + "/<FILESTEM>_{methodValue}.png",
            uid=[],
        ),
    ]

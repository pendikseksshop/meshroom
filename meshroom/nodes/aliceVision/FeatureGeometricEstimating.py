__version__ = "2.0"

from meshroom.core import desc
from meshroom.core.utils import DESCRIBER_TYPES, VERBOSE_LEVEL


class FeatureGeometricEstimating(desc.AVCommandLineNode):
    commandLine = 'aliceVision_featureGeometricEstimating {allParams}'
    size = desc.DynamicNodeSize('input')
    parallelization = desc.Parallelization(blockSize=20)
    commandLineRange = '--rangeStart {rangeStart} --rangeSize {rangeBlockSize}'

    category = 'Sparse Reconstruction'
    documentation = '''
    Estimating the relative constraints between pairs of images
'''

    inputs = [
        desc.File(
            name="input",
            label="SfMData",
            description="Input SfMData file.",
            value="",
        ),
        desc.ListAttribute(
            elementDesc=desc.File(
                name="featuresFolder",
                label="Features Folder",
                description="Folder containing some extracted features and descriptors which will be used for estimating the best geometric constraint.",
                value="",
            ),
            name="featuresFolders",
            label="Features Folders",
            description="Folder(s) containing the extracted features and descriptors which will be used for estimating the best geometric constraint.",
            exposed=True,
        ),
        desc.ListAttribute(
            elementDesc=desc.File(
                name="matchesFolder",
                label="Estimation Matches Folder",
                description="",
                value="",
            ),
            name="matchesFolders",
            label="Estimation Matches Folders",
            description="Folder(s) in which the computed matches which will be used for estimating the best geometric constraint are stored.",
            exposed=True,
        ),
        desc.File(
            name="imagePairsList",
            label="Image Pairs",
            description="Path to a file which contains the list of image pairs to match.",
            value="",
        ),
        desc.ChoiceParam(
            name="describerTypes",
            label="Describer Types",
            description="Describer types used to describe an image.",
            values=DESCRIBER_TYPES,
            value=["dspsift"],
            exclusive=False,
            joinChar=",",
            exposed=True,
        ),
        desc.ChoiceParam(
            name="geometricEstimator",
            label="Geometric Estimator",
            description="Geometric estimator:\n"
                        " - acransac: A-Contrario Ransac.\n"
                        " - loransac: LO-Ransac (only available for 'fundamental_matrix' model).",
            value="acransac",
            values=["acransac", "loransac"],
            advanced=True,
        ),
        desc.ChoiceParam(
            name="geometricFilterType",
            label="Geometric Filter Type",
            description="Geometric validation method to filter features matches:\n"
                        " - fundamental_matrix\n",
            value="fundamental_matrix",
            values=["fundamental_matrix"],
            advanced=True,
        ),
        desc.IntParam(
            name="maxIteration",
            label="Max Iterations",
            description="Maximum number of iterations allowed in the Ransac step.",
            value=50000,
            range=(1, 100000, 1),
            advanced=True,
        ),
        desc.FloatParam(
            name="geometricError",
            label="Geometric Validation Error",
            description="Maximum error (in pixels) allowed for features matching during geometric verification.\n"
                        "If set to 0, it will select a threshold according to the localizer estimator used\n"
                        "(if ACRansac, it will analyze the input data to select the optimal value).",
            value=0.0,
            range=(0.0, 10.0, 0.1),
            advanced=True,
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
            label="Constraints Folder",
            description="Path to a folder in which the computed constraints are stored.",
            value=desc.Node.internalFolder,
        ),
    ]

__version__ = "1.0"

from meshroom.core import desc

class Split360Images(desc.CommandLineNode):
	commandLine = 'aliceVision_utils_split360Images {allParams}'
	
	category = 'Utils'
	documentation = '''This node is used to extract multiple images from equirectangular or dualfisheye images or image folder'''

	inputs = [
		desc.File(
			name='input',
			label='Images Folder',
			description="Images Folder",
			value='',
			uid=[0],
		),
		desc.ChoiceParam(
			name='splitMode',
			label='Split Mode',
			description="Split mode (equirectangular, dualfisheye)",
			value='equirectangular',
			values=['equirectangular', 'dualfisheye'],
			exclusive=True,
			uid=[0],
		),
		desc.ChoiceParam(
			name='dualFisheyeSplitPreset',
			label='Dual Fisheye Split Preset',
			description="Dual-Fisheye split type preset (center, top, bottom)",
			value='center',
			values=['center', 'top', 'bottom'],
			exclusive=True,
			uid=[0],
		),
		desc.IntParam(
			name='equirectangularNbSplits',
			label='Equirectangular Nb Splits',
			description="Equirectangular number of splits",
			value=2,
			range=(1, 100, 1),
			uid=[0],
		),
		desc.IntParam(
			name='equirectangularSplitResolution',
			label='Equirectangular Split Resolution',
			description="Equirectangular split resolution",
			value=1200,
			range=(100, 10000, 1),
			uid=[0],
		),
		desc.BoolParam(
			name='equirectangularDemoMode',
			label='Equirectangular Demo Mode',
			description="Export a SVG file that simulates the split",
			value=False,
			uid=[0],
		),
	]

	outputs = [
		desc.File(
			name='output',
			label='Output Folder',
			description="Output folder for extracted frames.",
			value=desc.Node.internalFolder,
			uid=[],
		),
	]
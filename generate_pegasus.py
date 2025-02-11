import sys
import os

from wfcommons import WorkflowGenerator
from wfcommons.generator import BLASTRecipe
from wfcommons.generator import BWARecipe
from wfcommons.generator import CyclesRecipe
from wfcommons.generator import EpigenomicsRecipe
from wfcommons.generator import GenomeRecipe
from wfcommons.generator import MontageRecipe
from wfcommons.generator import SeismologyRecipe
from wfcommons.generator import SoyKBRecipe
from wfcommons.generator import SRASearchRecipe

def generate(nbtasks,nbiter): 
	factor=1.6
	for i in range(29,30):
		print(i)

		recipe = BWARecipe.from_num_tasks(num_tasks=nbtasks, runtime_factor=700*factor)
		generator = WorkflowGenerator(recipe)
		work = generator.build_workflow()
		work.write_json('workflowhub/files/BWAR/n'+(str)(nbtasks)+'f'+(str)(factor)+'_'+(str)(i)+'.json')

		recipe = CyclesRecipe.from_num_tasks(num_tasks=nbtasks, runtime_factor=360*factor)
		generator = WorkflowGenerator(recipe)
		work = generator.build_workflow()
		work.write_json('workflowhub/files/Cycles/n'+(str)(nbtasks)+'f'+(str)(factor)+'_'+(str)(i)+'.json')




generate((int) (sys.argv[1]), (int) (sys.argv[2]))


from app import app, Movies, Index
from Query_Evaluation import QueryEvaluation

query = ''
while (query != 'q'):
	query = input ("Query: ")
	result_list = QueryEvaluation(query, Index, Movies)  
	print(result_list)
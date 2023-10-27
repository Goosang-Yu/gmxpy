import gmxpy
import pandas as pd

def make_decomp_df(file:str, silence=True):
    '''GBSA decomposition results file 
    분석을 위해 dataframe이 인식할 수 있는 csv 파일로 만드는 객체

    ## Data example ##
    | Run on Fri Oct 27 19:17:14 2023\n
    | GB non-polar solvation energies calculated with gbsa=2\n
    idecomp = 3: Pairwise decomp adding 1-4 interactions to Internal.\n
    Energy Decomposition Analysis (All units kcal/mol): Generalized Born model\n

    DELTAS:\n
    Total Energy Decomposition:\n
    Resid 1,Resid 2,Internal,,,van der Waals,,,Electrostatic,,,Polar Solvation,,,Non-Polar Solv.,,,TOTAL,,\n
    ,,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean,Avg.,Std. Dev.,Std. Err. of Mean\n
    R:A:ARG:351,R:A:ARG:351,0.0,0.0,0.0,0.0,0.5897586551665688,0.015222429700453965,0.0,6.785105251173467,0.1751322965612053,2.9772637441705534,3.1993571192946018,0.08257952368898057,1.0425542756210526,0.6088115226883254,0.01571420872548597,4.019818019791606,7.549305000315245,0.19485727534109232\n
    R:A:ARG:351,R:A:ASN:355,0.0,0.0,0.0,0.0,0.1863456749011414,0.0048098216301125886,0.0,0.6239917901458101,0.016106030960193803,0.01945755229846769,0.6328086828777381,0.016333606305824484,0.0033432117553630915,0.135970829538314,0.0035095820567055645,0.022800764053830778,0.9181641249441898,0.023698997416992967\n
    ...
    '''

    try: 
        f = open(f"{file}_summary.csv", 'x', encoding='utf-8')
        
        header_1 = []
        header_2 = []
        columns  = []
        line_cnt = 0

        for line in open(f'./{file}.dat'):
            
            line_cnt += 1
            
            if   line_cnt > 9 : f.write(line)
            elif line_cnt == 8: header_1 = line.replace('\n','').split(',')
            elif line_cnt == 9: 
                header_2 = line.split(',')
                for h1, h2 in zip(header_1, header_2):
                    if len(h1) >  0: _h1 = h1
                    if len(h2) == 0: columns.append(_h1)
                    else           : columns.append(f'{_h1}_{h2}')
                        
                columns = ','.join(columns)
                f.write(columns)
            
            elif line_cnt <  5: 
                if silence == False: print(line, end='')
                
        f.close()
        
    except: pass

    df = pd.read_csv(f"{file}_summary.csv")    

    return df
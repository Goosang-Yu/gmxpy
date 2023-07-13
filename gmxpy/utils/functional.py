import gmxpy
import pandas as pd

class xvg2df:
    '''.xvg file to pd.DataFrame convertor'''
    
    def __init__(self, file:str):

        self.cfg = {

            # For plot
            'colormap'  : 'winter',
            'legend_loc': '', 
        }

        with open(file, 'r') as file:
            lines = file.readlines()

        data = [line.split() for line in lines if not line.startswith('@') and not line.startswith('#')]
        n_data = len(data[0]) - 1
        
        # 그래프 정보 추출
        labelds   = {}
        dict_data = {}

        for line in lines:
            if line.startswith('@    title'):
                self.title = line.split('"')[1]
            elif line.startswith('@    xaxis  label'):
                self.x_label = line.split('"')[1]
                labelds['x_label'] = self.x_label
            elif line.startswith('@    yaxis  label'):
                self.y_label = line.split('"')[1]
            elif line.startswith('@ s') and 'legend' in line:
                _order, _label = line.split(sep='@ s')[1].split('legend')
                labelds['y_legend_'+str(int(_order)+1)] = _label.split('"')[1]
        

        for n in range(n_data + 1):
            
            # x_data
            if n == 0: dict_data[self.x_label] = [float(row[0]) for row in data]

            # y_data
            else:
                try   : dict_data[labelds['y_legend_%s' % n]] = [float(row[n]) for row in data]
                except: dict_data['%s_%s' % (self.y_label, n)] = [float(row[n]) for row in data]

            label_key = 'y_legend_%s' % n

        self.data = pd.DataFrame(dict_data).set_index(self.x_label)

    # End: __init__

    def __call__(self):
        print('Data title: ', self.title)
        
        return self.data
    
    def plot(self):

        self.data.plot(xlabel   = self.x_label,
                       ylabel   = self.y_label,
                       colormap = self.cfg['colormap'],

                       ).legend(loc=(1.05, 0.5),
                                )
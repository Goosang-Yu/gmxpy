import gmxpy
import matplotlib.pyplot as plt


def plot_xvg(filename, color='k'):
    '''.xvg 파일을 읽고 matplotlib.pyplot으로 그래프를 그려주는 함수. 
    Grace 파일을 볼 수 없는 환경에서 그래프를 보고 분석하기에 유용하게 쓸 수 있다. 
    .xvg 파일 내에는 각종 정보들이 @ tag를 이용해서 나타나있는데, 각 tag의 정보에 따라서 그려주는 그래프 형태가 달라진다. 

    예를 들어, @TYPE에는 이 그래프가 어떤 형태인지 나와있는데, 대부분의 경우에는 xy 그래프이다. 
    xy 그래프인 경우에는 x축 값 / y축 값 각각을 가져오고, 이를 그래프로 그려준다. 
    '''

    with open(filename, 'r') as file:
        lines = file.readlines()

    # 그래프 정보 추출
    title = None
    x_label = None
    y_label = None
    plot_type = None
    legend_labels = []
    legend = None
    data_start = None
    plot_legend = False
    color = color

    for line in lines:
        if line.startswith('@    title'):
            title = line.split('"')[1]
        elif line.startswith('@    xaxis'):
            x_label = line.split('"')[1]
        elif line.startswith('@    yaxis'):
            y_label = line.split('"')[1]
        elif line.startswith('@TYPE'):
            plot_type = line.split()[-1]
        elif line.startswith('@ legend on'):
            plot_legend = True
        elif line.startswith('@ s'):
            legend_labels.append(line.split('"')[1])


    # 데이터 추출
    data = [line.split() for line in lines if not line.startswith('@') and not line.startswith('#')]
    x_data = [float(row[0]) for row in data]
    y_data = [float(row[1]) for row in data]

    # 그래프 그리기
    if plot_type == 'xy':
        if len(legend_labels) == 0: legend = 'Value'
        else                      : legend = legend_labels[0]
        plt.plot(x_data, y_data, color, label=legend)
    elif plot_type == 'bar':
        plt.bar(x_data, y_data)
    # 다른 plot_type에 대한 처리 추가 가능
    else:
        plt.plot(x_data, y_data,  color, label=legend)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if plot_legend:
        plt.legend()

    plt.show()

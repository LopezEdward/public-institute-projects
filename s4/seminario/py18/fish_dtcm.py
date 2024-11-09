from sklearn.tree import DecisionTreeClassifier, plot_tree, DecisionTreeRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.pyplot import savefig as py_save_fig
from matplotlib.pyplot import clf as clear_canvas
from matplotlib.pyplot import figure as py_figure
from pandas import DataFrame, Series, read_csv
from numpy import meshgrid as np_meshgrid, array as np_array, ndarray, linspace as np_linspace, round as np_round
from pathlib import Path
from os.path import exists as os_exists
from os import makedirs as os_makedirs
from datetime import datetime
from codec import ClassCodec
from counter import Counter
from threading import Thread, 
from time import sleep

SELF_PATH:Path = Path(__file__).parent
DATA_PATH:Path = SELF_PATH.joinpath("data")
CODEC:ClassCodec = ClassCodec()
__df:DataFrame = None

def __create_dirs (path:Path) -> None:
    if not isinstance(path, Path) and not path.is_dir():
        raise ValueError()

    os_makedirs(path, exist_ok=True)

def read_file (file_path: Path) -> DataFrame:
    path:Path = file_path if file_path != None and file_path.is_file() else SELF_PATH.joinpath("data", "Fish.csv")

    if path.suffix[1:] != "csv":
        raise ValueError()

    df:DataFrame = read_csv(path) if __df == None else __df

    return df

def get_train_test_data1(df:DataFrame, localCopy:bool = False) -> tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    k:DataFrame = df.copy() if localCopy else df

    k["Species"] = CODEC.code_all(k["Species"].values)
    # Predict with weight
    #print(k["Species"])
    
    #exit(100)

    x_train, x_test, y_train, y_test = train_test_split(k.drop(["Species"], axis=1), k["Species"], test_size=.7)

    return (x_train, x_test, y_train, y_test)

def get_train_test_data2(df:DataFrame, localCopy:bool = False) -> tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    # Cause of error => One set of data has 0 data in Weigth column
    k:DataFrame = df.copy() if localCopy else df

    k["Weight"] = k["Weight"][k["Weight"] > 0]
    #k.drop(["Species"], inplace=True, axis=1)
    k.dropna(axis=0, inplace=True)
    # THE MOST VALUED CLASS = CodecClass
    k["Species"] = CODEC.code_all(k["Species"].values)

    x_train, x_test, y_train, y_test = train_test_split(k.drop(["Weight"], axis=1), k["Weight"], test_size=.7)

    return (x_train, x_test, y_train, y_test)

def paint_and_save(fig:Figure, title:str, file_ext:str = "png", append_to_name:str = None, name_prefix:str = "MODEL_DT", dtm:datetime = None) -> Path:
    OUTPATH:Path = DATA_PATH.joinpath("output")
    IMG_OUTPUT:Path = OUTPATH.joinpath("img")
    
    if not IMG_OUTPUT.exists():
        __create_dirs(IMG_OUTPUT)

    dt:datetime = datetime.today() if dtm == None else dtm
    tmp:str = "" if append_to_name == None else append_to_name + "_" if not append_to_name.endswith("_") else append_to_name
    name:str = f"{name_prefix}_{tmp}{dt.year}-{dt.month}-{dt.day}_{dt.hour}h-{dt.minute}m-{dt.second}s.{file_ext}"

    if fig != None:
        fig.suptitle(title)
        fig.savefig(IMG_OUTPUT.joinpath(name), dpi=200)
    else:
        py_save_fig(IMG_OUTPUT.joinpath(name), dpi=200)

    clear_canvas()

    return IMG_OUTPUT.joinpath(name)

def score_model(model:DecisionTreeClassifier|DecisionTreeRegressor, x_test:DataFrame, y_test:Series) -> float:
    y_predict:Series = model.predict(x_test)

    return accuracy_score(y_test, y_predict)

def make_frequency_data(model:DecisionTreeClassifier|DecisionTreeRegressor|LinearRegression, x_test:DataFrame, fig:Figure = None, plot_colocation: tuple[int, int, int] = (1, 1, 1), **kargs) -> Axes:
    fig:Figure = py_figure() if fig == None or not isinstance(fig, Figure) else fig

    if len(plot_colocation) != 3:
        raise ValueError()

    ax:Axes = fig.add_subplot(plot_colocation[0], plot_colocation[1], plot_colocation[2])
    tmp_name:str = None
    
    if isinstance(model, DecisionTreeRegressor) or isinstance(model, LinearRegression):
        ax.hist(model.predict(x_test), edgecolor="black")
        tmp_name = "Decision Tree Regressor" if isinstance(model, DecisionTreeRegressor) else "Linear Regression"
    elif isinstance(model, DecisionTreeClassifier):
        data_predict:list[int] = model.predict(x_test)
        decode_data:list[str] = CODEC.decode_all(data_predict)
        counter:Counter = Counter.counter_of_values(decode_data)
        tmp_name = "Decision Tree Classifier"

        bars = ax.bar(counter.get_count_object(), counter.get_value_count_object())
        ax.bar_label(bars, padding=3) 
    else:
        raise ValueError()

    tm:str = model._in_data.get('name', '') if hasattr(model, "_in_data") else ""
    ax.set_title(f"Frequency of {tmp_name} {tm}".strip())
    ax.set_xlabel("Weight")
    ax.set_ylabel("Frequency")

    return ax


# Independent code block
def make_regression_data3D(df:DataFrame = None) -> LinearRegression:
    raise NotImplementedError()
    
    labels_x:list[str] = ["Height", "Width"]
    labels_y:list[str] = ["Weight"]

    df:DataFrame = read_file(DATA_PATH.joinpath("Fish.csv")) if df == None else df
    df.drop(["Species", "Length1", "Length2", "Length3"], axis=1, inplace=True)
    df = df[df["Weight"] > 0]
    
    # Code of aegis4048
    #   GitHub: https://github.com/aegis4048
    train, test = train_test_split(df, train_size=.7)
    #print(train);
    #print();
    #print(test);
    #exit(100)
    lin_model:LinearRegression = LinearRegression().fit(train.get(labels_x), train.get(labels_y))
    fig:Figure = Figure()

    #print(test.get(labels_x[0]).to_numpy(), test.get(labels_x[1]).to_numpy()); exit(100)
    
    

    xx_pred, yy_pred = np_meshgrid(test.get(labels_x[0]).to_numpy(), test.get(labels_x[1]).to_numpy())
    model_viz = np_array([xx_pred.flatten(), yy_pred.flatten()]).T
    y_predict = lin_model.predict(model_viz)

    #print(xx_pred.__len__()); print(); print(yy_pred.__len__())
    #print(model_viz.__len__()); print(model_viz.__len__())
    #print(y_predict.__len__()); exit(0)

    #print(y_predict.__len__()); exit(100)
    print("Calcs finish. Render...")

    ax1:Axes = fig.add_subplot(projection="3d")
    
    #ax1.scatter(test.get(labels_x[0]), test.get(labels_x[1]), y_predict, facecolor=(0,0,0,0), s=20, edgecolor='red')
    ax1.scatter(xx_pred.flatten(), yy_pred.flatten(), y_predict, facecolor=(0,0,0,0), s=20, edgecolor='red')
    ax1.plot(test.get(labels_x[0]).to_numpy(), test.get(labels_x[1]).to_numpy(), test.get(labels_y[0]).to_numpy(), linestyle="None", marker="o", alpha=.5, color="k", zorder=15)
    ax1.view_init(elev=32, azim=135)

    ax1.set_xlabel(labels_x[0])
    ax1.set_ylabel(labels_x[1])
    ax1.set_zlabel(labels_y[0])

    ax1.locator_params(nbins=4, axis='x')
    ax1.locator_params(nbins=5, axis='x')

    dt:datetime = datetime.today()

    paint_and_save(fig, "Cosas", dtm=dt, name_prefix="MODEL_LR")

    print("Render finish.")
    #for i in range(360):
    #    ax1.view_init(elev=32, azim=i)
    #    paint_and_save(fig, "Cosas", dtm=dt, append_to_name=f"{i}", name_prefix="MODEL_LR_GIF")

    return lin_model

def make_regression_data2D(df:DataFrame = None) -> tuple[LinearRegression, LinearRegression]:
    label_y:str = "Weight"
    label_x1, label_x2 = ("Height","Width")

    dfx1:DataFrame = df[df[label_y] > 0][[label_x1, label_y]]
    dfx2:DataFrame = df[df[label_y] > 0][[label_x2, label_y]]

    x_train1, x_test1, y_train1, y_test1 = [value.to_numpy().reshape(-1, 1) for value in train_test_split(dfx1.get(label_x1), dfx1.get(label_y), train_size=.7, test_size=.3)]
    x_train2, x_test2, y_train2, y_test2 = [value.to_numpy().reshape(-1, 1) for value in train_test_split(dfx2.get(label_x2), dfx2.get(label_y), train_size=.7, test_size=.3)]

    lin_model1:LinearRegression = LinearRegression().fit(x_train1, y_train1)
    lin_model2:LinearRegression = LinearRegression().fit(x_train2, y_train2)

    y_predict1:ndarray = lin_model1.predict(x_test1)
    y_predict2:ndarray = lin_model2.predict(x_test2)

    r_sqr1, r_sqr2 = np_round(lin_model1.score(x_test1, y_test1), 2), np_round(lin_model2.score(x_test2, y_test2), 2)
    #acc_score1, acc_score2 = accuracy_score(y_test1, y_predict1), accuracy_score(y_test2, y_predict2)

    fig:Figure = Figure()
    fig2:Figure = Figure()
    #fig.subplots_adjust(wspace=.5, hspace=.5)
    dtm:datetime = datetime.today()

    ax1_plot:Axes = fig.add_subplot(1, 2, 1)
    ax1_plot.scatter(x_test1, y_test1, color="red")
    ax1_plot.plot(x_test1, y_predict1)
    ax1_plot.set_title(f"R^2 = {r_sqr1}")
    ax1_plot.set_xlabel("Height")
    ax1_plot.set_ylabel("Weight")
    ax1_fd:Axes = make_frequency_data(lin_model1, x_test1, fig, (1, 2, 2))

    ax2_plot:Axes = fig2.add_subplot(1, 2, 1)
    ax2_plot.scatter(x_test2, y_test2, color="red")
    ax2_plot.plot(x_test2, y_predict2)
    ax2_plot.set_title(f"R^2 = {r_sqr2}")
    ax2_plot.set_xlabel("Width")
    ax2_plot.set_ylabel("Weight")
    ax2_fd:Axes = make_frequency_data(lin_model2, x_test2, fig2, (1, 2, 2))

    #ax2_plot:Axes = fig2.add_subplot(1, 1, 1)
    #ax2_plot.scatter(x_test2, y_test2, color="red")
    #ax2_plot.plot(x_test2, y_predict2)
    #ax2_fd:Axes = make_frequency_data(lin_model2, x_test2, fig2, (2, 1, 1), r2=np_round(r_sqr2, 2))

   #fig.tight_layout(h_pad=12)
    #fig2.tight_layout(h_pad=12)
    th1:Thread = Thread(None, paint_and_save, args=(fig, "Renders", "png"), kwargs={"name_prefix": "Custom", "append_to_name": "1", "dtm": dtm})
    th2:Thread = Thread(None, paint_and_save, args=(fig2, "Renders", "png"), kwargs={"name_prefix": "Custom", "append_to_name": "2", "dtm": dtm})
    
    th1.start(); th2.start();
    th1.join(); th2.join();

    return (lin_model1, lin_model2)

def execute (save_graphic:bool, img_format:str = "png", with_weight:bool = True) -> DecisionTreeClassifier|DecisionTreeRegressor:
    df:DataFrame = read_file(DATA_PATH.joinpath("Fish.csv"))

    x_train, x_test, y_train, y_test = get_train_test_data2(df, True) if with_weight else get_train_test_data1(df, True)

    model:DecisionTreeRegressor|DecisionTreeClassifier = DecisionTreeRegressor(max_leaf_nodes=20) if with_weight else DecisionTreeClassifier(max_leaf_nodes=20)
    model.fit(x_train, y_train)

    if save_graphic:
        plot_tree(model, rounded=True, feature_names=x_train.columns.values, class_names=CODEC.get_keys(in_tuple=True), filled=True) 

    ap_name:str = "with_weight" if with_weight else "with_class"
    pt:Path = paint_and_save(None, "Decision Tree", img_format, ap_name) if save_graphic else None

    if save_graphic:
        print(f"DT Model {pt.upper()} in {pt.__str__()}")

    model._in_data:object = {"name": ap_name, "test_data": {"x": x_test, "y": y_test}} # Add new attribute

    return model


#model1:DecisionTreeClassifier = execute(False,img_format="svg", with_weight = False)
#model2:DecisionTreeRegressor = execute(False, img_format="svg", with_weight=True)
#
#fig:Figure = Figure()
#fig.set_layout_engine("tight")
#make_frequency_data(model1, model1._in_data.get("test_data").get("x"), fig, (2, 1, 1))
#make_frequency_data(model2, model2._in_data.get("test_data").get("x"), fig, (2, 1, 2))
#
#fig.savefig(DATA_PATH.joinpath("output", "img", "pi.svg"))
__df:DataFrame = read_file(DATA_PATH.joinpath("Fish.csv")) if __df == None else __df

make_regression_data2D(__df)
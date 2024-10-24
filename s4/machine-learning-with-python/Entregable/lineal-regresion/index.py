from numpy import ndarray, array
from pathlib import Path
from sklearn.linear_model import LinearRegression
from pandas import DataFrame, read_csv, read_excel
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from os import makedirs
from os.path import exists as os_exists

SELFPATH:Path = Path(__file__).parent
DATAPATH:Path = SELFPATH.joinpath("data")

class Index:
    def __init__(self):
        pass

    def execute(self, data_path:Path|str, outfile_path:Path|str, outfile_name:str, createDirectory:bool = True, file_ext:str = "csv") -> None:
        tmp:str = data_path.__str__()
        tmp += "." + file_ext if not tmp.endswith(file_ext) else None
        
        data_path:Path = Path(tmp)
        print(data_path)
        if not os_exists(data_path):
            raise IOError()

        self.__data_path:Path = Path(data_path)
        self.__outfile_path:Path = Path(outfile_path)
        self.__outfile_name:str = outfile_name
        self.__create_dir_if_not_exists:bool = createDirectory
        self.__data_file_ext:str = file_ext

        self.__data:DataFrame = self.__load_data()

        self.__main__()

    def __main__ (self) -> None:
        self.__model_lr:LinearRegression = LinearRegression()

        counter:int = 1
        ls:list = []

        for _ in self.__data["Fecha"]:
            ls.append(counter)
            counter += 1

        ls:ndarray = array(ls).reshape(-1, 1)

        #x_train, x_test, y_train, y_test = train_test_split(self.__data["Fecha"], self.__data["Total"], train_size=8/10, test_size=2/10)

        self.__model_lr.fit(ls, self.__data["Total"])
        predict_data = self.__model_lr.predict(ls)

        figure:Figure = Figure()
        ax:Axes = figure.add_subplot(1, 1, 1)
        
        ax.scatter(ls, self.__data["Total"])
        ax.plot(predict_data, c="red")
        ax.set_xlabel("Días")
        ax.set_ylabel("Total de la venta")
        ax.set_title("Relación entre los N° de ventas y total de la venta")

        path = self.__paint_and_save_plot(figure)

        print("Image saved in " + path.__str__())

    def __load_data (self) -> DataFrame:
        df:DataFrame = None

        match self.__data_file_ext:
            case "csv":
                df = read_csv(self.__data_path)
            case "xlsx":
                df = read_excel(self.__data_path)
            case _:
                raise ValueError()

        return df

    def __paint_and_save_plot (self, figure:Figure) -> Path:
        figure.set_size_inches(10, 10, True)
        path:Path = None

        if not self.__outfile_path.exists():
            if self.__create_dir_if_not_exists:
                self.__create_dirs(self.__outfile_path)
        
        full_outfile:Path = self.__outfile_path.joinpath(self.__outfile_name)
        
        figure.savefig(full_outfile)

        path = full_outfile
        
        return path
    
    def __create_dirs (self, dir_path:Path) -> None:
        makedirs(dir_path)

a = Index()
a.execute(DATAPATH.joinpath("dataCGP"), DATAPATH.joinpath("img", "test"), "my_file.png", True)
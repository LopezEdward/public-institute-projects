from pandas import read_csv, read_excel, DataFrame, Series
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.pyplot import clf as clear_canvas, savefig as py_save_fig, figure as py_figure
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from pathlib import Path
from os import makedirs as os_makedirs
from os.path import exists
from datetime import datetime
from threading import Thread, current_thread
from typing import Hashable, Iterable, Tuple, TypeVar, Generic, TypeVarTuple, TypedDict, Callable
from numpy import round as np_round, ndarray, array as np_array

#DefinedMap = TypedDict("DefinedMap", {key:Hashable, values:tuple[object, object]})
#
#class Pair:
#    def __init__(self):
#        self.__map:DefinedMap = dict()
#
#    def add_pair(self, key:Hashable, value1:object, value2:object, replace_key_values:bool = False) -> None:
#        if not isinstance(key, Hashable):
#            raise ValueError()
#
#        if replace_key_values:
#            self.__map[key] = (value1, value2)
#            return None
#
#        if not key in self.__map.keys():
#            self.__map[key] = (value1, value2)
#
#    def get_pair(self, key:Hashable) -> Tuple:
#        if not isinstance(key, Hashable):
#            raise ValueError()
#
#        if key in self.__map.keys():
#            return self.__map[key]
#
#        return None

class ThreadPool:
    def __init__(self, initial_n_threads:int = 5):
        self.__pool:list[Thread] = [Thread() for _ in range(initial_n_threads)]
        self.__initial_n_threads:int = initial_n_threads

    def execute_task(self, func_target:Callable, *args, **kwargs) -> Thread:
        for item in self.__pool:
            if not item.is_alive():
                item = Thread(target=func_target, args=args, kwargs=kwargs)
                item.start()
                return item

        nw_thread:Thread = Thread(target=func_target, args=args, kwargs=kwargs)

        return nw_thread


class Main:
    def __init__(self, fileName:str, fileExt:str, dataPath:Path = None, outputPath:Path = None):
        self.__dir_path:Path = Path(__file__).parent
        self.__data_path:Path = dataPath if isinstance(dataPath, Path) and dataPath.exists() and dataPath.is_dir() else self.__dir_path.joinpath("data") 
        self.__output_path:Path = outputPath if isinstance(outputPath, Path) and outputPath.exists() and outputPath.is_dir() else self.__data_path.joinpath("output")
        self.__data_file:Path = self.__data_path.joinpath(f"{fileName}.{fileExt}")

        if not self.__data_path.exists():
            os_makedirs(self.__data_path)

        if not self.__output_path.exists():
            os_makedirs(self.__output_path)

        self.__main_df:DataFrame = self.__read_file()
        self.__main_fg:Figure = Figure()
        #self.__pairs:Pair = Pair()
        self.__threads_pool:ThreadPool = ThreadPool(3)
        self.__output_suffix_uid:int = 0

    def execute (self, *iterables:Iterable[str]) -> None:
        for it in iterables:
            #print(it); continue


            if not isinstance(it, Iterable):
                raise ValueError()

            if not (it.__len__() >= 2 and it.__len__() <= 3):
                raise ValueError()

            data:tuple[DataFrame, DataFrame, DataFrame, DataFrame] = self.__get_train_test_set_2D(target_columns=it, test_size=.3)

            #for i in data:
            #    print(i)

            #exit(100)

            self.__threads_pool.execute_task(self.__do_in_thread, data, x_col_name=it[0], y_col_name=it[1], append_name=str(self.__output_suffix_uid))

            self.__output_suffix_uid += 1
            

    def __do_in_thread(self, data:tuple[DataFrame, DataFrame, DataFrame, DataFrame], x_col_name:str = None, y_col_name:str = None, append_name:str = None) -> None:
        fig:Figure = Figure()
        dtm:datetime = datetime.today()

        self.action_linear_regression_2D_inthreads(fig, (1, 1, 1), data, x_col_name=x_col_name, y_col_name=y_col_name, append_name=append_name)
        
        th:Thread = current_thread()

        print(f"{th.name}({th.native_id}) [INFO] :: Imaged saved in {self.__paint_and_save(fig, f'Linear Regression of relation within {x_col_name} - {y_col_name}', append_to_name=append_name, dtm=dtm)}")

    def action_linear_regression_2D_inthreads(self, fig:Figure, fig_position:tuple[int, int, int | tuple[int, int]], data:tuple[DataFrame, DataFrame, DataFrame, DataFrame], x_col_name:str = None, y_col_name:str = None, append_name:str = None) -> None:
        lr:LinearRegression = LinearRegression().fit(data[0].to_numpy().reshape(-1, 1), data[2])
        y_predict:ndarray = lr.predict(data[1].to_numpy().reshape(-1, 1))

        #print(y_predict); exit(100)
        
        ax:Axes = fig.add_subplot(fig_position[0], fig_position[1], fig_position[2])
        ax.scatter(data[1], data[3], color="red")
        ax.plot(data[1], y_predict, color="k")
        ax.set_xlabel(x_col_name)
        ax.set_ylabel(y_col_name)

    
    def __action_linear_regression_2D(self, data:tuple[DataFrame, DataFrame, DataFrame, DataFrame], return_value:bool = False, x_col_name:str = None, y_col_name:str = None, fig_position:tuple[int, int, int|tuple[int, int]] = (1, 1, 1)) -> tuple[tuple[DataFrame, DataFrame, DataFrame, DataFrame], LinearRegression]|None:
        lr:LinearRegression = LinearRegression().fit(data[0], data[2])
        y_predict:ndarray = lr.predict(data[1])

        ax:Axes = self.__main_fg.add_subplot(fig_position)
        ax.scatter(data[1], data[3], color="red")
        ax.plot(data[1], y_predict, color="k")

        return tuple([data, lr]) if return_value else None

    def __get_train_test_set_2D(self, df:DataFrame = None, target_columns:tuple[str, str] = None, test_size:float = 0.7) -> tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
        

        if target_columns is None or (target_columns.__len__() > 2 and target_columns.__len__() <= 3):
            raise ValueError()

        lc_df:DataFrame = df if not df is None else self.__main_df.copy()
        unused_columns:list[str] = [x for x in lc_df.columns if x not in target_columns]
        lc_df.drop(unused_columns, axis=1, inplace=True)

        #print(lc_df.head()); print(target_columns); #exit(100)

        if target_columns.__len__() == 3:
            return train_test_split(lc_df[target_columns[0], target_columns[1]], lc_df[target_columns[2]])

        return train_test_split(lc_df.get(target_columns[0]), lc_df.get(target_columns[1]), test_size=test_size)

    def __paint_and_save(self, fig:Figure, title:str, file_ext:str = "png", append_to_name:str = None, name_prefix:str = "MODEL_LR", dtm:datetime = None, clear_figure:bool = False) -> Path:
        OUTPATH:Path = self.__data_path.joinpath("output")
        IMG_OUTPUT:Path = self.__output_path.joinpath("img")
        
        if not IMG_OUTPUT.exists():
            os_makedirs(IMG_OUTPUT)

        dt:datetime = datetime.today() if dtm == None else dtm
        tmp:str = "" if append_to_name == None else append_to_name + "_" if not append_to_name.endswith("_") else append_to_name
        name:str = f"{name_prefix}_{tmp}{dt.year}-{dt.month}-{dt.day}_{dt.hour}h-{dt.minute}m-{dt.second}s.{file_ext}"

        if fig != None:
            fig.suptitle(title)
            fig.savefig(IMG_OUTPUT.joinpath(name), dpi=200)

            fig.clear() if clear_figure else None
        else:
            py_save_fig(IMG_OUTPUT.joinpath(name), dpi=200)

        clear_canvas()

        return IMG_OUTPUT.joinpath(name)
    
    def create_dirs (self, dirPath:Path) -> None:
        if not dirPath.exits():
            os_makedirs(dirPath)

    def __read_file(self) -> DataFrame:
        df:DataFrame = None

        match self.__data_file.suffix[1:]:
            case "xlsx":
                df = read_excel(self.__data_file)
            case _:
                raise ValueError()

        return df

mn:Main = Main("ejercicio 2", "xlsx")
mn.execute(("Horas Trabajadas", "Productos Terminados"), ("Horas Descanso", "Productos Terminados"), ("Semana", "Horas Trabajadas"), ("Horas Trabajadas", "Horas Descanso"), ("Semana", "Horas Descanso"))
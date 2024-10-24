from pandas import DataFrame, read_csv, read_excel
from sklearn.cluster import KMeans
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pathlib import Path
from os.path import exists as os_exists
from os import makedirs

SELFPATH:Path = Path(__file__).parent
DATAPATH:Path = SELFPATH.joinpath("data")

class Index:
    def __init__(self):
        pass

    def execute(self, data_path:Path|str, outfile_path:Path|str, outfile_name:str, createDirectory:bool = True, file_ext:str = "csv", n_clusters:int=3) -> None:
        tmp:str = data_path.__str__()

        if not tmp.endswith(file_ext):
            tmp += "." + file_ext
        
        data_path:Path = Path(tmp)
        #print(data_path)
        if not os_exists(data_path):
            raise IOError()

        self.__data_path:Path = Path(data_path)
        self.__outfile_path:Path = Path(outfile_path)
        self.__outfile_name:str = outfile_name
        self.__create_dir_if_not_exists:bool = createDirectory
        self.__data_file_ext:str = file_ext
        self.__kmeans_max_clusters:int = n_clusters

        self.__data:DataFrame = self.__load_data()

        self.__main__()

    def __main__(self):
        self.__data.drop(labels=["address"], axis=1, inplace=True)

        self.__model_kmeans = KMeans(self.__kmeans_max_clusters).fit(self.__data.to_numpy())
        self.__data["cluster_id"] = self.__model_kmeans.labels_
        fig:Figure = Figure()

        ax1:Axes = fig.add_subplot(1, 1, 1)

        # This section is copy for another development's code.
        # Credits: CodigoMaquina
        # Social Media:
        # - Youtube: CodigoMaquina [https://www.youtube.com/@CodigoMaquina]
        # - GitHub: Código Maquina [https://github.com/CodigoMaquina]
        #
        # Link of repository's file where I get code:
        # -> Python File: https://github.com/CodigoMaquina/code/blob/main/machine_learning_python/k-medias.ipynb
        # 
        # <--- START OF COPY --->
        colors:list[str] = ["red", "blue", "orange", "green", "blue", "green"]

        for cluster in range(self.__kmeans_max_clusters):
            data_tmp:DataFrame = self.__data[self.__data["cluster_id"] == cluster]

            ax1.scatter(data_tmp["construction_year"], data_tmp["now_value"], color=colors[cluster], alpha=0.6)
            ax1.scatter(self.__model_kmeans.cluster_centers_[cluster][0], self.__model_kmeans.cluster_centers_[cluster][1], color=colors[cluster], marker="P", s=280)

        # <--- END OF COPY --->

        ax1.set_title("Agrupaciones de relacion entre el precio de una vivienda y su año de construcción")
        ax1.set_xlabel("Año de Construcción")
        ax1.set_ylabel("Precio actual")

        print("Image saved in " + self.__paint_and_save_plot(fig).__str__())


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
    
    def __create_dirs (self, dir_path:Path) -> None:
        makedirs(dir_path)

ind:Index = Index()
ind.execute(DATAPATH.joinpath("data.csv"), DATAPATH.joinpath("img", "test"), "test.png", True)
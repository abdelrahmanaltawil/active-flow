# env imports
import yaml
import pathlib
import numpy as np
import neptune.new as neptune

# local imports
import algorithm_tasks as task
import helpers.register as re
import postprocessing


if __name__ == "__main__":

    run = neptune.init_run(
        source_files=["./src/simulation"],
        tags=["reference simulation"]
    )

    # Preprocessing
    with open(pathlib.Path("./parameters/simulation.yml"), "r") as file:
        parameters = yaml.safe_load(file)

        discretization = parameters["algorithm"]["discretization"]
        physical = parameters["algorithm"]["physical"]
    
    run["parameters"] = parameters["algorithm"]
    re.init_register()


    # Algorithm
    task.discretize(
        L= discretization["domain_length"],
        N= discretization["collocation_points_per_axis"] 
    )
    task.set_initial_conditions(
        N= discretization["collocation_points_per_axis"]
    )
    v_eff = task.model_problem(
        k_norm= np.sqrt(re.register["k_vectors"][:,:,0]**2 + re.register["k_vectors"][:,:,1]**2),
        K_MIN= physical["k_min"],
        K_MAX= physical["k_max"], 
        V_0= physical["v_0"], 
        V_RATIO= physical["v_ratio"]
    )    
    task.prepare_stepping_scheme(
        STEPPING_SCHEME= discretization["time_stepping_scheme"], 
        v_eff= re.register["v_eff"], 
        k_vectors= re.register["k_vectors"], 
        COURANT= discretization["courant"],
        h = discretization["domain_length"]/discretization["collocation_points_per_axis"],
        N= discretization["collocation_points_per_axis"]
        )
    monitored, snapshots = task.solve(
        w_k= re.register["initial_w_k"],
        ITERATIONS= discretization["iterations"],
        tau= discretization["tau"],
        time_step= re.register["time_step"],
        velocity= re.register["cal_velocity"],
        cfl_controller= re.register["cfl_controller"],
        energy= re.register["cal_energy"]
        )


    # Postprocessing
    postprocessing.save_arrays(
        operators= [
            (re.register["x_vectors"], "x_vectors"),
            (re.register["k_vectors"], "k_vectors")
            ], 
        snapshots= snapshots,
        headers= parameters["postprocessing"]["save_quantities"],
        save_path= pathlib.Path(parameters["postprocessing"]["save_path"])
        )
    run["data/arrays"].upload_files(parameters["postprocessing"]["save_path"]+"/arrays")

    monitor_table = postprocessing.save_monitoring_table(
        monitored_data= monitored,
        headers= ["Iterations"]+parameters["preprocessing"]["monitor"],
        save_path= pathlib.Path(parameters["postprocessing"]["save_path"])
        )
    run["data/tables/monitoring"].upload(parameters["postprocessing"]["save_path"]+"/tables/monitoring.csv")
    
    run.wait()
    postprocessing.remove_data(
        data_path= pathlib.Path(parameters["postprocessing"]["save_path"])
        )

    figure = postprocessing.plot_convergence(
        monitored_data= monitor_table,  
    )
    run["plots/convergence"].upload(figure)
    
    run.stop()
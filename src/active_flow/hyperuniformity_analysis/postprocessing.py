import pathlib 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.fftpack as scipy
import scipy.stats as scipy_stats


# local imports
import active_flow.hyperuniformity_analysis.algorithm_tasks as task



def plot_structure_factor_snapshots(structure_factor: dict, symbol: str) -> list[plt.figure]:
    '''
    Placeholder 
    '''

    # define style
    plt.style.use([
        './config/matplotlib/main.mplstyle',
        './config/matplotlib/snapshots.mplstyle'
        ])

    if len(structure_factor) > 6:
        indices = np.round(np.linspace(0, len(structure_factor)-1, 6)).astype(int)
        structure_factor = {key: value for i, (key, value) in enumerate(structure_factor.items()) if i in indices}
    
    figure, ax = plt.subplots(2,3)
    figure.suptitle(symbol, fontweight="bold")
    
    for i, (key, value) in enumerate(structure_factor.items()):
        
        _plot_structure_factor(
            ax= ax.flatten()[i],
            structure_factor= scipy.fftshift(value[symbol]),
            iteration= key
            )

    return figure


def _plot_structure_factor(ax: plt.Axes, structure_factor: np.ndarray, iteration: str) -> None:
    '''
    Placeholder
    '''

    ax.imshow(
        structure_factor,
        extent=[0, 2*np.pi, 0, 2*np.pi],
        cmap="gray"
        )

    ax.set(
        title= iteration,
        xticks=[0, np.pi, 2*np.pi],
        xticklabels=["$-k$", "0", "$k$"],
        yticks=[0, np.pi, 2*np.pi],
        yticklabels=["", "0", "$k$"]
        )


def plot_radial_profile_snapshots(k_modes: np.ndarray, radial_profile_snapshots: dict, extrapolation_line: list, symbol: str) -> plt.figure:
    '''
    Placeholder
    '''

    # define style
    plt.style.use([
        './config/matplotlib/main.mplstyle',
        './config/matplotlib/scatter.mplstyle'
        ])

    figure, ax = plt.subplots()

    if len(radial_profile_snapshots) > 6:

        accumulated_quantity = np.zeros_like(k_modes) 
        for i, (snapshot_key, snapshot_value) in enumerate(radial_profile_snapshots.items()):
            
            ax.plot(
                k_modes,
                snapshot_value[symbol], 
                "o",
                markersize=5,
                mfc="none",
                color="lightgray",
                )  
            
            accumulated_quantity = accumulated_quantity + snapshot_value[symbol]
            if i == len(radial_profile_snapshots)-1: 
                ax.plot(
                    k_modes,
                    accumulated_quantity/len(radial_profile_snapshots), 
                    "o",
                    markersize=5,
                    color="red",
                    label= "Averaged Value"
                    )
    
    else:    
        for snapshot_key, snapshot_value in radial_profile_snapshots.items():

            ax.plot(
                k_modes,
                snapshot_value[symbol], 
                "o",
                markersize=5,
                mfc="none",
                label= snapshot_key
                )

    slop, y_intercept = extrapolation_line
    f = lambda x: slop*x + y_intercept
    ax.plot(
        k_modes,
        f(k_modes),
        "r--"
        )

    ax.annotate(
       "$S(k=0) =$"+" {:.2E}".format(y_intercept),
       xy= (np.mean(k_modes), f(np.mean(k_modes))),
       xytext=(0, -15),
       textcoords='offset points',
       fontsize=12,
       bbox= {
        "boxstyle": "round",
        "facecolor": "white",
        "alpha": 0.8
       }
    )

    ax.set(
        xlabel= r"$k$",
        ylabel= r"$S(k)$" 
        )

    ax.legend(loc="lower right")

    return figure


def plot_normalized_radial_profile_snapshots(k_modes: np.ndarray, radial_profile_snapshots: dict, extrapolation_line: list, symbol: str) -> plt.figure:
    '''
    Placeholder
    '''

    # define style
    plt.style.use([
        './config/matplotlib/main.mplstyle',
        './config/matplotlib/scatter.mplstyle'
        ])

    figure, ax = plt.subplots()

    s_k_max_global=0
    k_max_global=0
    if len(radial_profile_snapshots) > 6:

        accumulated_quantity = np.zeros_like(k_modes) 
        for i, (snapshot_key, snapshot_value) in enumerate(radial_profile_snapshots.items()):
            
            s_k_max = np.max(snapshot_value[symbol])
            k_max_index = np.where(snapshot_value[symbol] == s_k_max)
            k_max = k_modes[k_max_index][0]
            
            ax.plot(
                k_modes/k_max,
                snapshot_value[symbol]/s_k_max, 
                "o",
                markersize=5,
                mfc="none",
                color="lightgray",
                )  
            
            accumulated_quantity = accumulated_quantity + snapshot_value[symbol]
            if i == len(radial_profile_snapshots)-1: 
                s_k_max = np.max(accumulated_quantity/len(radial_profile_snapshots))
                k_max_index = np.where(accumulated_quantity/len(radial_profile_snapshots) == s_k_max)
                k_max = k_modes[k_max_index][0]

                ax.plot(
                    k_modes/k_max,
                    (accumulated_quantity/len(radial_profile_snapshots))/s_k_max, 
                    "o",
                    markersize=5,
                    color="red",
                    label= "Averaged Value"
                    )
            
            if s_k_max > s_k_max_global:
                s_k_max_global = s_k_max
            if k_max > k_max_global:
                k_max_global = k_max
    
    else: 
        for snapshot_key, snapshot_value in radial_profile_snapshots.items():
            
            s_k_max = np.max(snapshot_value[symbol])
            k_max_index = np.where(snapshot_value[symbol] == s_k_max)
            k_max = k_modes[k_max_index][0]
            
            ax.plot(
                k_modes/k_max,
                snapshot_value[symbol]/s_k_max, 
                "o",
                markersize=5,
                mfc="none",
                label= snapshot_key
                )

            if s_k_max > s_k_max_global:
                s_k_max_global = s_k_max
            if k_max > k_max_global:
                k_max_global = k_max

    slop, y_intercept = extrapolation_line
    f = lambda x: slop*x + y_intercept
    
    k_normalized = k_modes/k_max_global
    N_k_extrapolation = f(k_normalized)

    plot_limit = np.where(N_k_extrapolation < 1)
    k_normalized = k_normalized[plot_limit]
    N_k_extrapolation = N_k_extrapolation[plot_limit]

    ax.plot(
        k_normalized,
        N_k_extrapolation,
        "r--"
        )

    ax.annotate(
       "$S(k=0) =$"+" {:.2E}".format(y_intercept),
       xy= (np.mean(k_normalized), f(np.mean(k_normalized))),
       xytext=(0, -15),
       textcoords='offset points',
       fontsize=12,
       bbox= {
        "boxstyle": "round",
        "facecolor": "white",
        "alpha": 0.8
       }
    )

    ax.set(
        xlabel= r"$k/K$",
        ylabel= r"$N(k)$"
        )

    ax.legend(loc="lower right")

    return figure


def plot_power_law_snapshots(k_modes: np.ndarray, radial_profile_snapshots: dict, extrapolation_line: list, symbol: str) -> plt.figure:
    '''
    Placeholder
    '''

    # define style
    plt.style.use([
        './config/matplotlib/main.mplstyle',
        './config/matplotlib/scatter.mplstyle'
        ])

    figure, ax = plt.subplots()

    if len(radial_profile_snapshots) > 6:

        accumulated_quantity = np.zeros_like(k_modes) 
        for i, (snapshot_key, snapshot_value) in enumerate(radial_profile_snapshots.items()):
            
            s_k_max = np.max(snapshot_value[symbol])
            k_max_index = np.where(snapshot_value[symbol] == s_k_max)
            k_max = k_modes[k_max_index][0]
            
            ax.plot(
                k_modes/k_max,
                snapshot_value[symbol]/s_k_max, 
                "o",
                markersize=5,
                mfc="none",
                color="lightgray",
                )  
            
            accumulated_quantity = accumulated_quantity + snapshot_value[symbol]
            if i == len(radial_profile_snapshots)-1: 
                s_k_max = np.max(accumulated_quantity/len(radial_profile_snapshots))
                k_max_index = np.where(accumulated_quantity/len(radial_profile_snapshots) == s_k_max)
                k_max = k_modes[k_max_index][0]

                ax.plot(
                    k_modes/k_max,
                    (accumulated_quantity/len(radial_profile_snapshots))/s_k_max, 
                    "o",
                    markersize=5,
                    color="red",
                    label= "Averaged Value"
                    )
                
                # interval = np.where((k_modes/k_max >= 1e-7) & (k_modes/k_max <= 1))
                # slop, y_intercept, r_value, p_value, std_err = scipy_stats.linregress(
                #     x= (k_modes/k_max)[interval],
                #     y= ((accumulated_quantity/len(radial_profile_snapshots))/s_k_max)[interval])

                # x1 = np.linspace(2, 20, num=50)
                # x2 = np.linspace(2, 20, num=50)
                # ax.loglog(x1, 1e-4*x1, color='k')
                # ax.loglog(x2, 1e1*x2**(-5/3), color='k')
                
                # ax.plot(
                #     k_modes/k_max,
                #     slop*(k_modes/k_max) + y_intercept, ==> a*x^b <==> a*x + b
                #     "r--"
                #     )
            
    else: 
        for snapshot_key, snapshot_value in radial_profile_snapshots.items():
            
            s_k_max = np.max(snapshot_value[symbol])
            k_max_index = np.where(snapshot_value[symbol] == s_k_max)
            k_max = k_modes[k_max_index][0]
            
            ax.plot(
                k_modes/k_max,
                snapshot_value[symbol]/s_k_max, 
                "o",
                markersize=5,
                mfc="none",
                label= snapshot_key
                )

    ax.set(
        xscale="log",
        yscale="log",
        xlabel= r"$k/K$",
        ylabel= r"$N(k)$",
        xlim=[1e-2,1],
        ylim= [1e-5,1]
        )


    ax.legend(loc="lower right")

    return figure


def plot_k_max_snapshots(k_modes: np.ndarray, radial_profile_snapshots: dict, symbol: str) -> plt.figure:
    '''
    Placeholder
    '''

    # define style
    plt.style.use([
        './config/matplotlib/main.mplstyle',
        ])

    if len(radial_profile_snapshots) > 6:
        indices = np.round(np.linspace(0, len(radial_profile_snapshots)-1, 6)).astype(int)
        radial_profile_snapshots = {key: value for i, (key, value) in enumerate(radial_profile_snapshots.items()) if i in indices}
    
    figure, ax = plt.subplots(figsize=(20,8))
    ax2 = ax.twinx()

    width = 7
    space = 1
    postions = np.linspace(0+3*width, len(radial_profile_snapshots)*(3*(width+space)), num= len(radial_profile_snapshots))
    
    s_k_max_snapshots=[]
    k_max_snapshots=[]
    for snapshot_key, snapshot_value in radial_profile_snapshots.items():
        
        s_k_max = np.max(snapshot_value[symbol])
        k_max_index = np.where(snapshot_value[symbol] == s_k_max)
        k_max = k_modes[k_max_index][0]

        s_k_max_snapshots.append(round(s_k_max, 3))
        k_max_snapshots.append(k_max)


    bar_s_k_max = ax.bar(
        x= postions-width,
        height= s_k_max_snapshots,
        width= width,
        label= "$\max(S(k))$",
        color= "k",
        edgecolor="k"
        )
    ax.bar_label(bar_s_k_max, padding=-40, color="w", fontweight="bold")

    bar_k_max = ax2.bar(
        x= postions,
        height= k_max_snapshots,
        width= width,
        label= "$\max(k)$",
        color= "gray",
        edgecolor="k"
        )
    ax2.bar_label(bar_k_max, padding=-40, color="w", fontweight="bold")

    ax2.set(
        ylabel= "$\max(k)$",
    )
    ax.set(
        xlabel= "Snapshots",
        ylabel= "$\max(S(k))$",
        xticks=postions,
        xticklabels= radial_profile_snapshots.keys()
    )
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")

    return figure


def compare_fitting_intervals(k: np.ndarray, radial_profile_snapshots: dict, intervals: list[list], symbol: str) -> np.ndarray:
    '''
    Placeholder
    '''

    # define style
    plt.style.use([
        './config/matplotlib/main.mplstyle',
        ])
    
    figure, ax = plt.subplots(figsize=(20,8))

    intervals_residuals=[]
    for interval in intervals:
        _, _, residuals = task.linear_curve_fitting(
            k= k,
            radial_profile_snapshots= radial_profile_snapshots, 
            k_interval= interval,
            symbol= symbol
        )

        intervals_residuals.append(residuals)

    width = 7
    space = 1
    postions = np.linspace(0+width, len(intervals_residuals)*((width+space)), num= len(intervals_residuals))
    
    bar_residuals = ax.bar(
        x= postions,
        height= intervals_residuals,
        width= width,
        label= symbol,
        color= "gray",
        edgecolor="k"
        )
    ax.bar_label(bar_residuals, padding=-40, color="w", fontweight="bold")


    ax.set(
        xlabel= "Fitting Intervals",
        ylabel= "Coefficient of Determination $R^2$",
        xticks=postions,
        xticklabels= [f"$k \in [{interval[0]},{interval[1]}]$" for interval in  intervals]
    )

    return figure
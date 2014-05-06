import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def pollen_to_sugar(harvest, pollens):
    for i in range(harvest.shape[0]):
        sugar_per_mg = pollens[pollens.id==harvest.pollen_id[i]].sugar_per_mg
        harvest.miligrams_harvested[i] *= sugar_per_mg
    return harvest


def filter_by_pullen_id(harvest, pollen_id):
    return harvest[harvest.pollen_id==pollen_id]


def total_sugar_from_pollen(harvest, pollen_id):
    return np.sum(filter_by_pullen_id(harvest, pollen_id).miligrams_harvested)

    
def total_clients_of_pollen(harvest, pollen_id):
   return filter_by_pullen_id(harvest, pollen_id).shape[0]


def total_sugar_per_day(harvest):
    unique_days = set(harvest.day)
    sugar_per_day = []
    for unique_day in unique_days:
        harvest_filter_day = harvest[harvest.day==unique_day]  
        sugar_per_day.append( [unique_day, np.sum(harvest_filter_day.miligrams_harvested) ])
    return sugar_per_day


def bees_effectiveness(harvest):
    unique_bees, unique_days = set(harvest.bee_id), set(harvest.day)
    bee_day = []
    for bee in unique_bees:
        harvest_filter_bee = harvest[harvest.bee_id==bee]  
        total_harvested = np.sum(harvest_filter_bee.miligrams_harvested)
        days_of_work = harvest_filter_bee.miligrams_harvested.shape[0]
        bee_day.append( [ bee, round(total_harvested,3), 
                               round(total_harvested/days_of_work ,3) , 
                               round(total_harvested/len(unique_days),3) ])
    return bee_day

#--------------------------------------------------------------------
def main():
    print 'Loading data,,,'
    harvest = pd.read_table('harvest.csv', sep=',')
    harvest.columns = ['bee_id', 'day', 'pollen_id', 'miligrams_harvested']
    pollens = pd.read_table('pollens.csv', sep=',')
    print harvest.shape, pollens.shape

    print 
    print 'Converting pollen[mg] to sugar[mg]'
    harvest = pollen_to_sugar(harvest, pollens)

    print
    print '1. Which pollen contributed the most sugar in total?'
    print '2. Which pollen was most popular among the bees?'

    pollen_table = []
    for pollen_id in range(1,pollens.shape[0]+1):
        pollen_table.append( [pollen_id, total_sugar_from_pollen(harvest, pollen_id), 
                                         total_clients_of_pollen(harvest, pollen_id)] )

    pollen_table = pd.DataFrame(pollen_table)
    pollen_table.columns = ['pollen_id', 'sugar', 'clients']
    print pollen_table
    print 'The most sugar contributer:', pollen_table.sugar.argmax()+1
    print 'The most popular:', pollen_table.clients.argmax()+1

    print '----------------------------------------'
    print '3. Which day was the best day for harvesting? Which one was the worst?'
    sugar_per_day = total_sugar_per_day(harvest)
    sugar_per_day = pd.DataFrame(sugar_per_day)
    sugar_per_day.columns = ['day', 'sugar']
    sugar_per_day = sugar_per_day.sort('day')

    worst_day_index, worst_day_sugar = sugar_per_day.sugar.argmin(), sugar_per_day.sugar.min()
    best_day_index, best_day_sugar = sugar_per_day.sugar.argmax(), sugar_per_day.sugar.max()
    print 'Worst day:', sugar_per_day.values[worst_day_index]
    print 'Best day', sugar_per_day.values[best_day_index]

    # plot sugar per day
    print 'Plotting...'
    plt.plot(range(sugar_per_day.shape[0]), sugar_per_day.sugar, color='#1f77b4')
    plt.title('Sugar per day')
    annotation_1 ="worst day [%s]" % (sugar_per_day.values[worst_day_index][0])
    plt.annotate(annotation_1, xy=(worst_day_index, worst_day_sugar), xytext=(worst_day_index-50, worst_day_sugar),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    annotation_2 ="best day [%s]" % (sugar_per_day.values[best_day_index][0])
    plt.annotate(annotation_2, xy=(best_day_index, best_day_sugar), xytext=(best_day_index-50, best_day_sugar),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.show()

    print '----------------------------------------'
    print '4. Which bee was most effective (udarnik), which one was the least' 
    print ' (effectiveness is measured as average sugar harvested per each working day).'
    
    bees_effect = pd.DataFrame( bees_effectiveness(harvest) )
    bees_effect.columns = ['Bee_id', 'Total', 'Avg_working_days', 'Avg_all_days']
    print bees_effect

    print
    print 'Most effective bee[working_days]:', bees_effect.Avg_working_days.argmax()+1, bees_effect.Avg_working_days.max()
    print 'Least effective bee[working_days]:', bees_effect.Avg_working_days.argmin()+1, bees_effect.Avg_working_days.min()
    print 'Most effective bee[working_days]:', bees_effect.Avg_all_days.argmax()+1, bees_effect.Avg_all_days.max()
    print 'Least effective bee[working_days]:', bees_effect.Avg_all_days.argmin()+1, bees_effect.Avg_all_days.min()

#------------------------------------------------
if __name__ == "__main__":
    main()

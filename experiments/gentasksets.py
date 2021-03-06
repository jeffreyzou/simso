#!/usr/bin/python
# coding=utf-8

import sys
import os
from simso.core import Model
from simso.configuration import Configuration
import simso.generator.task_generator as task_generator

def main(argv):
    print("usage: ./gen [tasksize] [num] [u] [min_p] [max_p] [outdir] [schduler1] [schduler2] ...")
    #outdir = input("Output directory: ")
    if argv and len(argv) > 7:
        n = int(argv[0])
        nsets = int(argv[1])
        u = float(argv[2])
        min_p = int(argv[3])
        max_p = int(argv[4])
        outdir = argv[5]
        schedulers = argv[6:]
    else:
        n = 7
        nsets = 10
        u = 1.99
        min_p = 70
        max_p = 500
        outdir = "tasksets"
        schedulers = [
            "simso.schedulers.RM"]
    #        "simso.schedulers.EDF",
    #        "simso.schedulers.RM_mono"]

    gensavetasksets(schedulers, n, nsets, u, min_p, max_p, outdir)

def gensavetasksets(schedulers, n, nsets, u, min_p, max_p, outdir):

    # Manual configuration:
    configuration = Configuration()
    configuration.duration = 1000 * configuration.cycles_per_ms

    u = task_generator.StaffordRandFixedSum(n, u, nsets)
    periods = task_generator.gen_periods_uniform_ex(n, nsets, min_p, max_p,
                                                 10000000, True)
    # Add processors.
    for i in range(1, 5):
        configuration.add_processor(name="CPU "+str(i), identifier=i)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    for i, exp_set in enumerate(task_generator.gen_tasksets(u, periods)):
        for scheduler_name in schedulers:
            configuration.scheduler_info.clas = scheduler_name
#            print("{}:".format(scheduler_name))
            while configuration.task_info_list:
                del configuration.task_info_list[0]
            id_ = 1
            for (c, p) in exp_set:
                configuration.add_task(name="T{}".format(id_), identifier=id_,
                                       period=p, activation_date=0, wcet=c,
                                       deadline=p, abort_on_miss=True)
                id_ += 1

            configuration.duration = configuration.get_hyperperiod() * configuration.cycles_per_ms
            
            # Vérification de la config.
            configuration.check_all()
            
            # save one taskset
            configuration.save(outdir+"/exp_{}.xml".format(i+1))

            # Initialisation de la simu à partir de la config.
#            model = Model(configuration)
            # Exécution de la simu.
#            try:
#                model.run_model()
#                print("Aborted jobs:", sum(
#                    model.results.tasks[task].exceeded_count
#                    for task in model.task_list))
#                assert sum(model.results.tasks[task].exceeded_count
#                           for task in model.task_list) == 0, "aborted jobs"
#            except AssertionError as e:
#                print(e)
#                configuration.save("exp_{}.xml".format(i))


if __name__ == "__main__":
    main(sys.argv[1:])

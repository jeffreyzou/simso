#!/usr/bin/python
# coding=utf-8

import sys
from simso.core import Model
from simso.configuration import Configuration
from simso.core import ProcEvent


def main(argv):
    if len(argv) == 1:
        configuration = Configuration(argv[0])
    else:
        # Configuration manuelle :
        configuration = Configuration()

        configuration.duration = 20 * configuration.cycles_per_ms

        # Ajout des tâches.
        configuration.add_task(name="T1", identifier=1, period=4,
                               activation_date=0, wcet=2, deadline=4)
        configuration.add_task(name="T2", identifier=2, period=5,
                               activation_date=0, wcet=1, deadline=5)
        configuration.add_task(name="T3", identifier=3, period=20,
                               activation_date=0, wcet=3, deadline=20)

        # Ajout d'un processeur.
        configuration.add_processor(name="CPU 1", identifier=1)
        configuration.add_processor(name="CPU 2", identifier=2)

        configuration.scheduler_info.clas ="simso.schedulers.RM"

        configuration.save("test.xml")

    # Vérification de la config.
    configuration.check_all()

    # Initialisation de la simu à partir de la config.
    model = Model(configuration)

    # Exécution de la simu.
    model.run_model()

    # Affichage des résultats.
    for log in model.logs:
        print(log)

    # Affichage de quelques métriques.
    # Durée d'exec des jobs
    print("Job computation times")
    for task in model.results.tasks:
        print(task.name + ":")
        for job in task.jobs:
            print("%s %.3f ms" % (job.name, job.computation_time))

    # Nombre de préemptions par task
    print("Preemption counts:")
    for task in model.results.tasks.values():
        print("%s %d" % (task.name, task.preemption_count))

    cxt = 0
    for processor in model.processors:
        prev = None
        for evt in processor.monitor:
            if evt[1].event == ProcEvent.RUN:
                if prev is not None and prev != evt[1].args.task:
                    cxt += 1
                prev = evt[1].args.task
    print("Number of context switches (without counting the OS): " + str(cxt))

if __name__ == "__main__":
    main(sys.argv[1:])

import os
import sys
import data_structures as ds


def read_template(filename: os.path) -> str:
    """

    :param filename:
    :return:
    """
    try:
        infile = open(filename, 'r')
    except OSError:
        print("* Error reading template file: {}".format(filename))
        sys.exit()

    content = infile.read()
    return content


def write_input_file(content: str, filename: os.path):
    """

    :param content: Information that shall be written into a file, expected
        to be string.
    :param filename: File name of the new file.
    :return: File written to specified location.
    """
    try:
        outfile = open(filename, 'w')
    except OSError:
        print("* Error writing input file: {}".format(filename))
        sys.exit()

    outfile.write(content)


def fill_place_holder(tc: str, place_holder: list) -> str:
    """

    :param tc: Content of the template file, including place holders.
    :param place_holder: List of place holders and values, to be exchanged.
    :return: New string where place holders are changed to values.
    """
    # TODO: check for place holder duplicates
    if place_holder is not None:
        for p in place_holder:
            tc = tc.replace("#" + p.place_holder + "#", str(p.value))
    else:
        print("Using empty list, place holders can't be changed.")

    return tc


def create_input_file(setup: SimulationSetup, tempfilename: os.path=None,
                      work_dir='execution'):
    """
    :param setup: specification of  SimulationSetup on which to base the
        simulation run
    :param tempfilename: Name of the FDS template.
    :param work_dir: flag to indicate if the regular execution of the function
        (in the sense of inverse modeling) is wanted or if only a simulation
        of the best parameter set is desired, range:['execution', 'best']
    :return: Saves a file that is read by the simulation software as input file
    """

    if not tempfilename:
        tempfilename = 'InputTemplate.fds'

    #
    # small test
    if work_dir == 'execution':
        wd = setup.execution_dir
    elif work_dir == 'best':
        wd = setup.best_dir
    #
    #

    # Log the set working directory
    logging.debug(wd)

    in_fn = setup.model_template
    template_content = read_template(in_fn)

    logging.debug(template_content)

    parameter_list = setup.model_parameter
    input_content = fill_place_holder(template_content, parameter_list)

    logging.debug(input_content)

    out_fn = os.path.join(wd, setup.model_input_file)

    write_input_file(input_content, out_fn)

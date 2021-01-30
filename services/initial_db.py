from domain.securities import initial_securities as securities_initial
from domain.industries import initial_industries as industries_initial


def initial(engine):
    securities_initial(engine)
    industries_initial(engine)

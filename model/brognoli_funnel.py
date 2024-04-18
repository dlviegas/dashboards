import pandas as pd

from core.mysql_conn import MySQLConnector


class BrognoliFunnel:

    def __init__(self):
        self.mysql_con = MySQLConnector()
        self.funnel = None
        self.raw = None
    def import_funnel(self):
        self.sent_funnel = self.mysql_con.select_table("select * from brognoli.disparos_funnel", True)
        self.delivered_funnel = self.mysql_con.select_table("select * from brognoli.entregue_funnel", True)
        self.opened_funnel = self.mysql_con.select_table("select * from brognoli.aberto_funnel", True)
        self.clicked_funnel = self.mysql_con.select_table("select * from brognoli.clicado_funnel", True)
        self.funnel = self.mysql_con.select_table("select * from brognoli.funnel_chart", True).loc[[3, 2, 0, 1]]
        self.period = self.mysql_con.select_table("select * from brognoli.period_interaction", True)
        # self.raw = self.mysql_con.select_table("select * from brognoli.brevo_raw", True)
        # self.raw['data_evento'] = self.raw['ts'].apply(lambda x: pd.to_datetime(x[:10], format='%d-%m-%Y'))
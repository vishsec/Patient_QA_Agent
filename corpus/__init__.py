import reportlab.rl_config as rl

rl.invariant = 1


# Had to add a regression testing because report_lab emnbed a wallclock timestamp inside the pdf despite not using datetime.now()
#discovered this while comparing hashes of the same file path - Path was same but the hashes different so had to fix it 
#ofc replay fictures dont rely on byte sof pdf instead on teh pdf texts itself but byte level stabiolity is nice to have. 
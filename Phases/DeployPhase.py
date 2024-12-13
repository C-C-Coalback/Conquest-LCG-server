

def deploy_phase(p_one, p_two):
    p_one_passed = False
    p_two_passed = False
    p_one.set_phase("Deploy")
    p_two.set_phase("Deploy")
    if p_one.get_initiative():
        p_one.set_turn(True)
        p_two.set_turn(False)
    else:
        p_one.set_turn(False)
        p_two.set_turn(True)
    while not p_one_passed or not p_two_passed:
        ret_val = p_one.take_deploy_turn()
        p_one_passed = True
        p_two_passed = True
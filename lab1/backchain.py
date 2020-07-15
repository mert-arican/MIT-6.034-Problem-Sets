from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def backchain_to_goal_tree(rules, hypothesis):
    all_consequents = [rule.consequent()[index] for rule in rules for index in range(0,len(rule.consequent()))]
    matched_rules = [rule for rule in rules if match(rule.consequent()[0], hypothesis) != None] ; chain = OR(hypothesis)
    for rule in matched_rules:
        bindings = get_bindings(rule.consequent(), hypothesis)
        template, antecedents = extract(rule.antecedent())
        for antecedent in antecedents:
            if antecedent_is_not_consequent_of_any_rule(all_consequents, antecedent):
                template.append(populate(antecedent, bindings))
            else:
                template.append(backchain_to_goal_tree(rules, populate(antecedent, bindings)))
        chain.append(template)
    return simplify(chain)

def extract(antecedent):
    return (type(antecedent)(), antecedent[:]) if isinstance(antecedent, list) else (OR() , [antecedent])
    
def antecedent_is_not_consequent_of_any_rule(consequents, antecedent):
    return not True in [match(consequent, antecedent) == None for consequent in consequents]

def get_bindings(consequents, hypothesis):
    return [match(consequent, hypothesis) for consequent in consequents if match(consequent, hypothesis) != None][0]

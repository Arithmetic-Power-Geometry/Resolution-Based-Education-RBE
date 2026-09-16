from rbe.obe import OBEStudent, calculate_co_results, attainment_level, weighted_po_attainment

def test_supplied_workbook_formula_pattern():
    students=[OBEStudent("1","A",{"CT1":10,"CT2":12,"Ass":8,"ESE":40})]
    max_marks={"CT1":15,"CT2":15,"Ass":10,"ESE":60}
    allocation={"CO1":{"CT1":4,"CT2":0,"Ass":3,"ESE":9}}
    rows,_=calculate_co_results(students,max_marks,allocation)
    expected=((10/15)*4+(12/15)*0+(8/10)*3+(40/60)*9)/(4+0+3+9)
    assert abs(rows[0]["CO1_score01"]-expected)<1e-12

def test_attainment_cutoffs_match_theory_of_computation_workbook():
    assert attainment_level(.60)==3
    assert attainment_level(.59)==2
    assert attainment_level(.50)==1
    assert attainment_level(.40)==0

def test_zero_mapping_denominator_returns_none_not_division_error():
    result=weighted_po_attainment({"CO1":2.0},{"CO1":{"PO8":0}})
    assert result["PO8"] is None

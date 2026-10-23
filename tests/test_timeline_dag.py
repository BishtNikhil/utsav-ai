import pytest
from app.services.timeline_dag import TimelineDAGService

def test_timeline_dag_generation_and_dependencies():
    dag = TimelineDAGService.generate_timeline("2027-04-30")

    assert dag.total_milestones == 7
    assert len(dag.critical_path_milestones) >= 4

    # Verify prerequisite dependencies
    venue_ms = [m for m in dag.milestones if m.milestone_id == "ms_lock_date_venue"][0]
    catering_ms = [m for m in dag.milestones if m.milestone_id == "ms_catering_tasting"][0]

    assert "ms_lock_date_venue" in catering_ms.dependencies
    assert len(venue_ms.dependencies) == 0

def test_timeline_shift_earlier():
    dag = TimelineDAGService.generate_timeline("2027-04-30")
    shifted_dag = TimelineDAGService.shift_timeline(dag, days_delta=-14)

    assert shifted_dag.target_date == "2027-04-16"
    assert shifted_dag.total_milestones == dag.total_milestones

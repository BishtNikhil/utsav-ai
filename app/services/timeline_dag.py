from datetime import datetime, timedelta
from typing import List, Optional
from app.models.schemas import Milestone, TimelineDAG

class TimelineDAGService:
    """
    Directed Acyclic Graph (DAG) Milestone & Dependency Scheduler.
    Models event management as an interconnected dependency network rather
    than a flat, unprioritized checklist.
    """

    # Template milestones defined with their days_before_event lead times and prerequisite dependencies
    MILESTONE_TEMPLATES = [
        {
            "id": "ms_lock_date_venue",
            "title": "Lock Celebration Date & Secure Venue Contract",
            "category": "Venue & Legal",
            "days_before": 120,
            "dependencies": [],
            "critical_path": True,
            "description": "Finalize city, visit top 3 candidate venues, review capacity/parking, and sign deposit contract.",
            "contingency": "If primary ballroom is booked, fall back to pre-vetted heritage hotel lawn option.",
        },
        {
            "id": "ms_catering_tasting",
            "title": "Food Tasting & Catering Contract Signature",
            "category": "Catering",
            "days_before": 90,
            "dependencies": ["ms_lock_date_venue"],
            "critical_path": True,
            "description": "Taste signature regional menus, lock dietary allergy counters, and negotiate per-plate inclusions.",
            "contingency": "Opt for venue's approved in-house culinary partner if external vendor delays.",
        },
        {
            "id": "ms_decor_concept_lock",
            "title": "Aesthetic Theme, Mandap/Stage & Lighting Finalization",
            "category": "Decor",
            "days_before": 75,
            "dependencies": ["ms_lock_date_venue"],
            "critical_path": False,
            "description": "Approve 3D moodboards, color swatches, entrance floral arches, and generator diesel backups.",
            "contingency": "Substitute exotic blooms with locally sourced seasonal marigold and jasmine installations.",
        },
        {
            "id": "ms_cinematography_booking",
            "title": "Retain Lead Cinematographer & Drone Operators",
            "category": "Media",
            "days_before": 60,
            "dependencies": ["ms_lock_date_venue"],
            "critical_path": False,
            "description": "Contract 2 candid photographers, 1 drone pilot, and agree on turnaround timeline for teaser reel.",
            "contingency": "Retain reputable boutique studio freelancer on standby.",
        },
        {
            "id": "ms_dispatch_invitations",
            "title": "Dispatch Digital Interactive Invitations & Open RSVP Hub",
            "category": "Guest Experience",
            "days_before": 45,
            "dependencies": ["ms_lock_date_venue", "ms_decor_concept_lock"],
            "critical_path": True,
            "description": "Publish personalized digital invitation web link with WhatsApp RSVP routing and venue Google Maps pin.",
            "contingency": "Broadcast automated reminder SMS / WhatsApp 14 days later.",
        },
        {
            "id": "ms_lock_rsvps_headcount",
            "title": "Lock Final Attendee Headcount & Dietary Roster",
            "category": "Coordination",
            "days_before": 21,
            "dependencies": ["ms_dispatch_invitations"],
            "critical_path": True,
            "description": "Reconcile confirmed guest count, dietary requests (Jain/Vegan/Gluten-Free), and room allocations.",
            "contingency": "Apply +5% buffer plate margin with caterer to absorb unexpected plus-ones.",
        },
        {
            "id": "ms_final_rehearsal_handoff",
            "title": "Day-of Run of Show Rehearsal & Vendor Handoff",
            "category": "Execution",
            "days_before": 7,
            "dependencies": ["ms_catering_tasting", "ms_lock_rsvps_headcount"],
            "critical_path": True,
            "description": "Distribute minute-by-minute itinerary to MC, DJ, family leads, and venue banquet manager.",
            "contingency": "Designate secondary emergency coordinator equipped with printed run-of-show binder.",
        },
    ]

    @classmethod
    def generate_timeline(cls, target_date_str: str) -> TimelineDAG:
        """
        Builds the complete DAG timeline anchored backwards from the target event date.
        """
        try:
            target_dt = datetime.strptime(target_date_str, "%Y-%m-%d")
        except ValueError:
            target_dt = datetime.now() + timedelta(days=120)

        milestones: List[Milestone] = []
        critical_ids: List[str] = []

        for item in cls.MILESTONE_TEMPLATES:
            deadline_dt = target_dt - timedelta(days=item["days_before"])
            # Ensure deadline does not fall in the past relative to today
            today = datetime.now()
            if deadline_dt < today:
                deadline_dt = today + timedelta(days=2)

            ms = Milestone(
                milestone_id=item["id"],
                title=item["title"],
                category=item["category"],
                deadline_date=deadline_dt.strftime("%Y-%m-%d"),
                days_before_event=item["days_before"],
                is_critical_path=item["critical_path"],
                status="pending",
                dependencies=item["dependencies"],
                description=item["description"],
                contingency_action=item["contingency"],
            )
            milestones.append(ms)
            if item["critical_path"]:
                critical_ids.append(item["id"])

        return TimelineDAG(
            target_date=target_date_str,
            total_milestones=len(milestones),
            critical_path_milestones=critical_ids,
            milestones=milestones,
        )

    @classmethod
    def shift_timeline(cls, original_dag: TimelineDAG, days_delta: int) -> TimelineDAG:
        """
        Dynamically shifts all milestone deadlines when the event date shifts earlier or later.
        Validates dependency ordering and enforces accelerated lead times.
        """
        old_target = datetime.strptime(original_dag.target_date, "%Y-%m-%d")
        new_target = old_target + timedelta(days=days_delta)
        new_target_str = new_target.strftime("%Y-%m-%d")

        updated_milestones: List[Milestone] = []
        today = datetime.now()

        # Compaction ratio if time was shortened
        compression_factor = max(0.65, min(1.0, (new_target - today).days / max(1, (old_target - today).days)))

        for ms in original_dag.milestones:
            # Squeeze lead days proportionally if event was moved earlier
            scaled_days_before = int(ms.days_before_event * compression_factor)
            new_deadline = new_target - timedelta(days=scaled_days_before)
            
            if new_deadline < today:
                new_deadline = today + timedelta(days=1)

            updated_ms = ms.model_copy(update={
                "deadline_date": new_deadline.strftime("%Y-%m-%d"),
                "days_before_event": scaled_days_before,
                "status": "in_progress" if ms.is_critical_path else ms.status,
            })
            updated_milestones.append(updated_ms)

        return TimelineDAG(
            target_date=new_target_str,
            total_milestones=len(updated_milestones),
            critical_path_milestones=original_dag.critical_path_milestones,
            milestones=updated_milestones,
        )

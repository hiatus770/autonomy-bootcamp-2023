"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own
        self.reached_waypoint = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        x_delta = 0
        y_delta = 0
        dist = float("inf")

        if not self.reached_waypoint:
            x_delta = self.waypoint.location_x - report.position.location_x
            y_delta = self.waypoint.location_y - report.position.location_y
            dist = x_delta * x_delta + y_delta * y_delta

        if self.reached_waypoint:
            print("waypoint reached")
            best_landing_pad = landing_pad_locations[0]

            # Calculate closest landing pad
            for landing_pad in landing_pad_locations:
                x_delta_landing = landing_pad.location_x - report.position.location_x
                y_delta_landing = landing_pad.location_y - report.position.location_y

                if (x_delta_landing**2 + y_delta_landing**2) < (
                    best_landing_pad.location_x**2 + best_landing_pad.location_y**2
                ):
                    best_landing_pad = landing_pad

            x_delta = best_landing_pad.location_x - report.position.location_x
            y_delta = best_landing_pad.location_y - report.position.location_y

        # Once we find closest landing pad and we already visited the waypoint we can land
        if dist < self.acceptance_radius**2 and self.reached_waypoint:
            command = commands.Command.create_land_command()
            return command

        # Once we've reached the waypoint we can now start looking at the nearest landing pads
        if dist < self.acceptance_radius**2 and not self.reached_waypoint:
            self.reached_waypoint = True

        if report.status == drone_status.DroneStatus.HALTED and dist > self.acceptance_radius**2:
            # we are currently stopped so check the next closest waypoint to our destination
            if (x_delta > 60 or x_delta < -60) or (y_delta > 60 or y_delta < -60):
                command = commands.Command.create_null_command()
                return command
            command = commands.Command.create_set_relative_destination_command(x_delta, y_delta)
        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

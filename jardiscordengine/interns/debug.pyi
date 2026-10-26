from collections.abc import Sequence

from jardiscordengine.interns.decorators import documented

@documented
class JDEDebug:

    def debug(
        self,
        *,
        is_colored: bool = False,
        max_depth: int = -1,
        branched_recursive: bool = False,
        show_root: bool = True,
    ) -> str:
        """
        Get a debug representation of the JDE object.

        Format:
            The debug representation uses a tree-like structure to display
            the object's identity, instance policy, decorators, and members.

            - Header:
                Displays the object's name when available, followed by its
                class name, instance policy, and registered decorators.

                Example:
                    my_object (JDEExample) {NORMAL:∞} | documented |  ‖ Example > InternBaseClass ‖

                The instance policy indicator shows the policy name and its
                instance limit:
                    NORMAL:∞       No instance limit.
                    UNIQUE:∞       No instance limit.
                    SINGLETON:1    One instance.
                    FLYWEIGHT:n    Maximum of n instances.

                Registered decorators are displayed between vertical bars.

            - Tree structure:
                Members are displayed beneath the header using tree branches:
                    ├─  A member with following siblings.
                    └─  The last member at the current level.
                    │   Vertical lines indicate continuing branches.

            - Member types:
                # :   JDEID, the object's internal identifier.
                ⚙ :   Properties.
                ⚐ :   Flags.
                ⏵ :   Fields.
                ◈ :   Other attributes.
                ƒ :   Methods, including their signatures and return types
                        when available.

            - Values:
                Values are displayed next to their corresponding member.
                Strings use their representation, booleans are displayed as
                True or False, and None is displayed explicitly.

                Dictionaries and sequences are displayed with their contents
                when expanded. Empty containers are identified as empty.
                Nested JDE objects are displayed recursively using the same
                format.

                External objects from PyCord and JarbinToolKit's classes
                include their type and source identification.

            - Recursive references:
                Recursive references are marked with <recursive> to indicate
                that an object has already been encountered in the current
                traversal path.

                When max_depth is reached, nested JDE objects are represented
                by [...] instead of expanding their members.

            - Errors:
                If a member cannot be retrieved, its value is displayed as
                <error: ...> rather than interrupting the debug output.

            - Colors:
                When is_colored is True, headers, member labels, values,
                instance policies, and errors are colored according to their
                categories. Otherwise, the output contains no debug colors.

        Args:
            is_colored (bool): Use colors for pretty printing.
            max_depth (int): Maximum exploration depth.
            branched_recursive (bool): Don't take in count the branches when exploring (allows an object to appear multiple times in debug mode).
            show_root (bool): Show the root JDE object.

        Returns:
            str: Debug string.
        """

__all__: Sequence[str] = [
    "JDEDebug",
]

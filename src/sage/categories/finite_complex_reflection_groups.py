r"""
Finite Complex Reflection Groups
"""
#*****************************************************************************
#       Copyright (C) 2011-2015 Christian Stump <christian.stump at gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.abstract_method import abstract_method
from sage.misc.all import prod
from sage.misc.cachefunc import cached_method
from sage.categories.category_with_axiom import CategoryWithAxiom
from sage.categories.coxeter_groups import CoxeterGroups

class FiniteComplexReflectionGroups(CategoryWithAxiom):
    r"""
    The category of finite complex reflection groups.

    See :class:`ComplexReflectionGroups` for the definition of complex
    reflection group. In the finite case, most of the information
    about the group can be recovered from its *degrees* and
    *codegrees*, and to a lesser extent to the explicit realization as
    subgroup of `GL(V)`. Hence the most important optional methods to
    implement are:

    - :meth:`ComplexReflectionGroups.Finite.ParentMethods.degrees`
    - :meth:`ComplexReflectionGroups.Finite.ParentMethods.codegrees`
    - :meth:`ComplexReflectionGroups.Finite.ElementMethods.to_matrix`

    Finite complex reflection groups are completely classified. In
    particular, if the group is irreducible, then it's uniquely
    determined by its degrees and codegrees and whether it's
    reflection representation is *primitive* or not (see [LT2009]_
    Chapter 2.1 for the definition of primitive).

    .. SEEALSO:: :wikipedia:`Complex_reflection_groups`

    EXAMPLES::

        sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
        sage: ComplexReflectionGroups().Finite()
        Category of finite complex reflection groups
        sage: ComplexReflectionGroups().Finite().super_categories()
        [Category of complex reflection groups,
         Category of finite groups,
         Category of finite finitely generated semigroups]

    An example of a finite reflection group::

        sage: W = ComplexReflectionGroups().Finite().example(); W
        Reducible real reflection group of rank 4 and type A2 x B2

        sage: W.reflections()
        Finite family {1: (1,8)(2,5)(9,12), 2: (1,5)(2,9)(8,12),
                       3: (3,10)(4,7)(11,14), 4: (3,6)(4,11)(10,13),
                       5: (1,9)(2,8)(5,12), 6: (4,14)(6,13)(7,11),
                       7: (3,13)(6,10)(7,14)}

    ``W`` is in the category of complex reflection groups::

        sage: W in ComplexReflectionGroups().Finite()
        True
    """
    def example(self):
        r"""
        Return an example of a complex reflection group.

        EXAMPLES::

            sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
            sage: ComplexReflectionGroups().Finite().example()
            Reducible real reflection group of rank 4 and type A2 x B2
        """
        from sage.combinat.root_system.reflection_group_real import ReflectionGroup
        return ReflectionGroup((1,1,3), (2,1,2))

    class SubcategoryMethods:

        @cached_method
        def WellGenerated(self):
            r"""
            Return the full subcategory of well-generated objects of ``self``.

            A finite complex generated group is *well generated* if it
            is isomorphic to a subgroup of the general linear group
            `GL_n` generated by `n` reflections.

            .. SEEALSO:: :meth:`ComplexRelfectionGroups.Finite.ParentMethods.is_well_generated`

            EXAMPLES::

                sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
                sage: C = ComplexReflectionGroups().Finite().WellGenerated(); C
                Category of well generated finite complex reflection groups

            Here is an example of a finite well-generated complex
            reflection group::

                sage: W = C.example(); W
                Reducible complex reflection group of rank 4 and type A2 x G(3,1,2)

            All finite Coxeter groups are well generated::

                sage: CoxeterGroups().Finite().is_subcategory(C)
                True
                sage: SymmetricGroup(3) in C
                True

            .. NOTE::

                The category of well generated finite complex
                reflection groups is currently implemented as an
                axiom. See discussion on :trac:`11187`. This may be a
                bit of overkill. Still it's nice to have a full
                subcategory.

            TESTS::

                sage: TestSuite(W).run()
                sage: TestSuite(ComplexReflectionGroups().Finite().WellGenerated()).run()
                sage: CoxeterGroups().Finite().WellGenerated.__module__
                'sage.categories.finite_complex_reflection_groups'

            We check that the axioms are properly ordered in
            ``sage.categories.category_with_axiom.axioms`` and yield
            desired output (well generated does not appear)::

                sage: CoxeterGroups().Finite()
                Category of finite coxeter groups
            """
            return self._with_axiom('WellGenerated')

    class ParentMethods:
        @abstract_method(optional=True)
        def degrees(self):
            r"""
            Return the degrees of ``self`` in increasing order.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4)
                sage: W.degrees()
                [2, 3, 4]

                sage: W = ColoredPermutations(3,3)
                sage: W.degrees()
                [3, 6, 9]

                sage: W = ReflectionGroup(31)
                sage: W.degrees()
                [8, 12, 20, 24]
            """

        @abstract_method(optional=True)
        def codegrees(self):
            r"""
            Return the codegrees of ``self`` in decreasing order.

            EXAMPLES::

                sage: W = ColoredPermutations(1,4)
                sage: W.codegrees()
                [2, 1, 0]

                sage: W = ColoredPermutations(3,3)
                sage: W.codegrees()
                [6, 3, 0]

                sage: W = ReflectionGroup(31)
                sage: W.codegrees()
                [28, 16, 12, 0]
            """

        def number_of_reflecting_hyperplanes(self):
            r"""
            Return the number of reflecting hyperplanes of ``self``.

            This is also the number of distinguished reflections.  For
            real groups, this coincides with the number of
            reflections.

            This implementation uses that it is given by the sum of
            the codegrees of ``self`` plus its rank.


            .. SEEALSO:: :meth:`number_of_reflections`

            EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: W.number_of_reflecting_hyperplanes()
                3
                sage: W = ColoredPermutations(2,3)
                sage: W.number_of_reflecting_hyperplanes()
                9
                sage: W = ColoredPermutations(4,3)
                sage: W.number_of_reflecting_hyperplanes()
                15
                sage: W = ReflectionGroup((4,2,3))
                sage: W.number_of_reflecting_hyperplanes()
                15
            """
            return sum(self.codegrees()) + self.rank()

        def number_of_reflections(self):
            r"""
            Return the number of reflections of ``self``.

            For real groups, this coincides with the number of
            reflecting hyperplanes.

            This implementation uses that it is given by the sum of
            the degrees of ``self`` minus its rank.

            .. SEEALSO:: :meth:`number_of_reflecting_hyperplanes`

            EXAMPLES::

                sage: [SymmetricGroup(i).number_of_reflections()
                ....:  for i in range(8)]
                [0, 0, 1, 1, 3, 6, 10, 15]

                sage: W = ColoredPermutations(1,3)
                sage: W.number_of_reflections()
                3
                sage: W = ColoredPermutations(2,3)
                sage: W.number_of_reflections()
                9
                sage: W = ColoredPermutations(4,3)
                sage: W.number_of_reflections()
                21
                sage: W = ReflectionGroup((4,2,3))
                sage: W.number_of_reflections()
                15
            """
            return sum(self.degrees()) - self.rank()

        def rank(self):
            r"""
            Return the rank of ``self``.

            The rank of ``self`` is the dimension of the smallest
            faithfull reflection representation of ``self``.

            This default implementation uses that the rank is the
            number of :meth:`degrees`.

            .. SEEALSO:: :meth:`ComplexReflectionGroups.rank`

            EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: W.rank()
                2
                sage: W = ColoredPermutations(2,3)
                sage: W.rank()
                3
                sage: W = ColoredPermutations(4,3)
                sage: W.rank()
                3
                sage: W = ReflectionGroup((4,2,3))
                sage: W.rank()
                3
            """
            return len(self.degrees())

        @cached_method
        def cardinality(self):
            r"""
            Return the cardinality of ``self``.

            It is given by the product of the degrees of ``self``.

            EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: W.cardinality()
                6
                sage: W = ColoredPermutations(2,3)
                sage: W.cardinality()
                48
                sage: W = ColoredPermutations(4,3)
                sage: W.cardinality()
                384
                sage: W = ReflectionGroup((4,2,3))
                sage: W.cardinality()
                192
            """
            from sage.rings.all import ZZ
            return ZZ.prod(self.degrees())

        def is_well_generated(self):
            r"""
            Return whether ``self`` is well-generated.

            A finite complex reflection group is *well generated* if
            the number of its simple reflections coincides with its rank.

            .. SEEALSO:: :meth:`ComplexReflectionGroups.Finite.WellGenerated`

            .. NOTE::

                - All finite real reflection groups are well generated.
                - The complex reflection groups of type `G(r,1,n)` and
                  of type `G(r,r,n)` are well generated.
                - The complex reflection groups of type `G(r,p,n)`
                  with `1 < p < r` are *not* well generated.

                - The direct product of two well generated finite
                  complex reflection group is still well generated.

            EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: W.is_well_generated()
                True

                sage: W = ColoredPermutations(4,3)
                sage: W.is_well_generated()
                True

                sage: W = ReflectionGroup((4,2,3))
                sage: W.is_well_generated()
                False

                sage: W = ReflectionGroup((4,4,3))
                sage: W.is_well_generated()
                True
            """
            return self.number_of_simple_reflections() == self.rank()

        def is_real(self):
            r"""
            Return whether ``self`` is real.

            A complex reflection group is *real* if it is isomorphic
            to a reflection group in `GL(V)` over a real vector space `V`.
            Equivalently its character table has real entries.

            This implementation uses the following statement: an
            irreducible complex reflection group is real if and only
            if `2` is a degree of ``self`` with multiplicity one.
            Hence, in general we just need to compare the number of
            occurences of `2` as degree of ``self`` and the number of
            irreducible components.

            EXAMPLES::

                sage: W = ColoredPermutations(1,3)
                sage: W.is_real()
                True

                sage: W = ColoredPermutations(4,3)
                sage: W.is_real()
                False

            .. TODO::

                 Add an example of non real finite complex reflection
                 group that is generated by order 2 reflections.
            """
            return self.degrees().count(2) == self.number_of_irreducible_components()

    class ElementMethods:

        @abstract_method(optional=True)
        def to_matrix(self):
            r"""
            Return the matrix presentation of ``self`` acting on a
            vector space `V`.

            EXAMPLES::

                sage: W = ReflectionGroup((1,1,3))
                sage: [t.to_matrix() for t in W]
                [
                [1 0]  [ 1  1]  [-1  0]  [-1 -1]  [ 0  1]  [ 0 -1]
                [0 1], [ 0 -1], [ 1  1], [ 1  0], [-1 -1], [-1  0]
                ]

                sage: W = ColoredPermutations(1,3)
                sage: [t.to_matrix() for t in W]
                [
                [1 0 0]  [1 0 0]  [0 1 0]  [0 0 1]  [0 1 0]  [0 0 1]
                [0 1 0]  [0 0 1]  [1 0 0]  [1 0 0]  [0 0 1]  [0 1 0]
                [0 0 1], [0 1 0], [0 0 1], [0 1 0], [1 0 0], [1 0 0]
                ]

            A different representation is given by the
            colored permutations::

                sage: W = ColoredPermutations(3, 1)
                sage: [t.to_matrix() for t in W]
                [[1], [zeta3], [-zeta3 - 1]]
            """

        def _matrix_(self):
            """
            Return ``self`` as a matrix.

            EXAMPLES::

                sage: W = ReflectionGroup((1,1,3))
                sage: [matrix(t) for t in W]
                [
                [1 0]  [ 1  1]  [-1  0]  [-1 -1]  [ 0  1]  [ 0 -1]
                [0 1], [ 0 -1], [ 1  1], [ 1  0], [-1 -1], [-1  0]
                ]
            """
            return self.to_matrix()

        def character_value(self):
            r"""
            Return the value at ``self`` of the character of the
            reflection representation given by :meth:`to_matrix`.

            EXAMPLES::

                sage: W = ColoredPermutations(1,3); W
                1-colored permutations of size 3
                sage: [t.character_value() for t in W]
                [3, 1, 1, 0, 0, 1]

            Note that this could be a different (faithful)
            representation than that given by the corresponding root
            system::

                sage: W = ReflectionGroup((1,1,3)); W
                Irreducible real reflection group of rank 2 and type A2
                sage: [t.character_value() for t in W]
                [2, 0, 0, -1, -1, 0]

                sage: W = ColoredPermutations(2,2); W
                2-colored permutations of size 2
                sage: [t.character_value() for t in W]
                [2, 0, 0, -2, 0, 0, 0, 0]

                sage: W = ColoredPermutations(3,1); W
                3-colored permutations of size 1
                sage: [t.character_value() for t in W]
                [1, zeta3, -zeta3 - 1]
            """
            return self.to_matrix().trace()

    class Irreducible(CategoryWithAxiom):

        def example(self):
            r"""
            Return an example of an irreducible complex reflection group.

            EXAMPLES::

                sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
                sage: ComplexReflectionGroups().Finite().Irreducible().example()
                Irreducible complex reflection group of rank 3 and type G(4,2,3)
            """
            from sage.combinat.root_system.reflection_group_real import ReflectionGroup
            return ReflectionGroup((4,2,3))

        class ParentMethods:
            def coxeter_number(self):
                r"""
                Return the Coxeter number of an irreducible
                reflection group.

                This is defined as `\frac{N + N^*}{n}` where
                `N` is the number of reflections, `N^*` is the
                number of reflecting hyperplanes, and `n` is the
                rank of ``self``.

                EXAMPLES::

                    sage: W = ReflectionGroup(31)
                    sage: W.coxeter_number()
                    30
                """
                return (self.number_of_reflecting_hyperplanes() + self.number_of_reflections()) // self.rank()

    class WellGenerated(CategoryWithAxiom):

        def example(self):
            r"""
            Return an example of a well-generated complex reflection group.

            EXAMPLES::

                sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
                sage: ComplexReflectionGroups().Finite().WellGenerated().example()
                Reducible complex reflection group of rank 4 and type A2 x G(3,1,2)
            """
            from sage.combinat.root_system.reflection_group_real import ReflectionGroup
            return ReflectionGroup((1,1,3), (3,1,2))

        class ParentMethods:
            def _test_well_generated(self, **options):
                """
                Check if ``self`` is well-generated.

                EXAMPLES::

                    sage: W = ReflectionGroup((3,1,2))
                    sage: W._test_well_generated()
                """
                tester = self._tester(**options)
                tester.assertEqual(self.number_of_simple_reflections(), self.rank())

            def is_well_generated(self):
                r"""
                Return ``True`` as ``self`` is well-generated.

                EXAMPLES::

                    sage: W = ReflectionGroup((3,1,2))
                    sage: W.is_well_generated()
                    True
                """
                return True

            coxeter_element = CoxeterGroups.ParentMethods.coxeter_element
            standard_coxeter_elements = CoxeterGroups.ParentMethods.standard_coxeter_elements

            @cached_method
            def coxeter_elements(self):
                r"""
                Return the (unique) conjugacy class in ``self`` containing all
                Coxeter elements.

                .. NOTE::

                    Beyond real reflection groups, the conjugacy class
                    is not unique and we only obtain one such class.

                EXAMPLES::

                    sage: W = ReflectionGroup((1,1,3))
                    sage: sorted(c.reduced_word() for c in W.coxeter_elements())
                    [[1, 2], [2, 1]]

                    sage: W = ReflectionGroup((1,1,4))
                    sage: sorted(c.reduced_word() for c in W.coxeter_elements())
                    [[1, 2, 3], [1, 2, 3, 1, 2], [2, 3, 1],
                     [2, 3, 1, 2, 1], [3, 1, 2], [3, 2, 1]]
                """
                return self.coxeter_element().conjugacy_class()

        class Irreducible(CategoryWithAxiom):
            r"""
            The category of finite irreducible well-generated
            finite complex reflection groups.
            """
            def example(self):
                r"""
                Return an example of an irreducible well-generated
                complex reflection group.

                EXAMPLES::

                    sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
                    sage: ComplexReflectionGroups().Finite().WellGenerated().Irreducible().example()
                    4-colored permutations of size 3
                """
                from sage.combinat.colored_permutations import ColoredPermutations
                return ColoredPermutations(4, 3)

            class ParentMethods:
                def coxeter_number(self):
                    r"""
                    Return the Coxeter number of a well-generated,
                    irreducible reflection group. This is defined to be
                    the order of a regular element in ``self``, and is
                    equal to the highest degree of ``self``.

                    .. SEEALSO:: :meth:`ComplexReflectionGroups.Finite.Irreducible`

                    .. NOTE::

                        This method overwrites the more general
                        method for complex reflection groups since
                        the expression given here is quicker to
                        compute.

                    EXAMPLES::

                        sage: W = ColoredPermutations(1,3)
                        sage: W.coxeter_number()
                        3

                        sage: W = ColoredPermutations(4,3)
                        sage: W.coxeter_number()
                        12

                        sage: W = ReflectionGroup((4,4,3))
                        sage: W.coxeter_number()
                        8
                    """
                    return max(self.degrees())

                def number_of_reflections_of_full_support(self):
                    r"""
                    Return the number of reflections with full
                    support.

                    EXAMPLES::

                        sage: W = ColoredPermutations(1,4)
                        sage: W.number_of_reflections_of_full_support()
                        1

                        sage: W = ColoredPermutations(3,3)
                        sage: W.number_of_reflections_of_full_support()
                        3
                    """
                    n = self.rank()
                    h = self.coxeter_number()
                    l = self.cardinality()
                    codegrees = self.codegrees()[:-1]
                    return n * h * prod(codegrees) // l

                @cached_method
                def rational_catalan_number(self, p, polynomial=False):
                    r"""
                    Return the ``p``-th rational Catalan number
                    associated to ``self``.

                    It is defined by

                    .. MATH::

                        \prod_{i = 1}^n \frac{p + (p(d_i-1)) \mod h)}{d_i},

                    where `d_1, \ldots, d_n` are the degrees and
                    `h` is the Coxeter number. See [STW2016]_
                    for this formula.

                    INPUT:

                    - ``polynomial`` -- optional boolean (default ``False``)
                      if ``True``, return instead the `q`-analogue as a
                      polynomial in `q`

                    REFERENCES:

                    .. [STW2016] C. Stump, H. Thomas, N. Williams.
                       *Cataland II*, in preparation, 2016.

                    EXAMPLES::

                        sage: W = ColoredPermutations(1,3)
                        sage: [W.rational_catalan_number(p) for p in [5,7,8]]
                        [7, 12, 15]

                        sage: W = ColoredPermutations(2,2)
                        sage: [W.rational_catalan_number(p) for p in [7,9,11]]
                        [10, 15, 21]

                    TESTS::

                        sage: W = ColoredPermutations(1,4)
                        sage: W.rational_catalan_number(3, polynomial=True)
                        q^6 + q^4 + q^3 + q^2 + 1
                    """
                    from sage.arith.all import gcd
                    from sage.combinat.q_analogues import q_int

                    h = self.coxeter_number()
                    if not gcd(h,p) == 1:
                        raise ValueError("parameter p = %s is not coprime to the Coxeter number %s" % (p, h))

                    if polynomial:
                        f = q_int
                    else:
                        f = lambda n: n

                    num = prod(f(p + (p * (deg - 1)) % h)
                               for deg in self.degrees())
                    den = prod(f(deg) for deg in self.degrees())
                    return num // den

                def fuss_catalan_number(self, m, positive=False,
                                        polynomial=False):
                    r"""
                    Return the ``m``-th Fuss-Catalan number
                    associated to ``self``.

                    This is defined by

                    .. MATH::

                        \prod_{i = 1}^n \frac{d_i + mh}{d_i},

                    where `d_1, \ldots, d_n` are the degrees and
                    `h` is the Coxeter number.

                    INPUT:

                    - ``positive`` -- optional boolean (default ``False``)
                      if ``True``, return instead the positive Fuss-Catalan
                      number
                    - ``polynomial`` -- optional boolean (default ``False``)
                      if ``True``, return instead the `q`-analogue as a
                      polynomial in `q`

                    See [Arm2006]_ for further information.

                    .. NOTE::

                        - For the symmetric group `S_n`, it reduces to the
                          Fuss-Catalan number `\frac{1}{mn+1}\binom{(m+1)n}{n}`.
                        - The Fuss-Catalan numbers for `G(r, 1, n)` all
                          coincide for `r > 1`.

                    REFERENCES:

                    .. [Arm2006] D. Armstrong. *Generalized noncrossing
                       partitions and combinatorics of Coxeter groups*.
                       Mem. Amer. Math. Soc., 2006.

                    EXAMPLES::

                        sage: W = ColoredPermutations(1,3)
                        sage: [W.fuss_catalan_number(i) for i in [1,2,3]]
                        [5, 12, 22]

                        sage: W = ColoredPermutations(1,4)
                        sage: [W.fuss_catalan_number(i) for i in [1,2,3]]
                        [14, 55, 140]

                        sage: W = ColoredPermutations(1,5)
                        sage: [W.fuss_catalan_number(i) for i in [1,2,3]]
                        [42, 273, 969]

                        sage: W = ColoredPermutations(2,2)
                        sage: [W.fuss_catalan_number(i) for i in [1,2,3]]
                        [6, 15, 28]

                        sage: W = ColoredPermutations(2,3)
                        sage: [W.fuss_catalan_number(i) for i in [1,2,3]]
                        [20, 84, 220]

                        sage: W = ColoredPermutations(2,4)
                        sage: [W.fuss_catalan_number(i) for i in [1,2,3]]
                        [70, 495, 1820]

                    TESTS::

                        sage: W = ColoredPermutations(2,4)
                        sage: W.fuss_catalan_number(2,positive=True)
                        330
                        sage: W = ColoredPermutations(2,2)
                        sage: W.fuss_catalan_number(2,polynomial=True)
                        q^16 + q^14 + 2*q^12 + 2*q^10 + 3*q^8 + 2*q^6 +
                        2*q^4 + q^2 + 1
                    """
                    h = self.coxeter_number()
                    if positive:
                        p = m * h - 1
                    else:
                        p = m * h + 1

                    return self.rational_catalan_number(p, polynomial=polynomial)

                def catalan_number(self, positive=False, polynomial=False):
                    r"""
                    Return the Catalan number associated to ``self``.

                    It is defined by

                    .. MATH::

                        \prod_{i = 1}^n \frac{d_i + h}{d_i},

                    where `d_1, \ldots, d_n` are the degrees and where
                    `h` is the Coxeter number.
                    See [Arm2006]_ for further information.

                    INPUT:

                    - ``positive`` -- optional boolean (default ``False``)
                      if ``True``, return instead the positive Catalan
                      number
                    - ``polynomial`` -- optional boolean (default ``False``)
                      if ``True``, return instead the `q`-analogue as a
                      polynomial in `q`

                    .. NOTE::

                        - For the symmetric group `S_n`, it reduces to the
                          Catalan number `\frac{1}{n+1} \binom{2n}{n}`.
                        - The Catalan numbers for `G(r,1,n)` all coincide
                          for `r > 1`.

                    EXAMPLES::

                        sage: [ColoredPermutations(1,n).catalan_number() for n in [3,4,5]]
                        [5, 14, 42]

                        sage: [ColoredPermutations(2,n).catalan_number() for n in [3,4,5]]
                        [20, 70, 252]

                        sage: [ReflectionGroup((2,2,n)).catalan_number() for n in [3,4,5]]
                        [14, 50, 182]

                    TESTS::

                        sage: W = ColoredPermutations(3,6)
                        sage: W.catalan_number(positive=True)
                        462
                        sage: W = ColoredPermutations(2,2)
                        sage: W.catalan_number(polynomial=True)
                        q^8 + q^6 + 2*q^4 + q^2 + 1
                    """
                    return self.fuss_catalan_number(1, positive=positive,
                                                    polynomial=polynomial)


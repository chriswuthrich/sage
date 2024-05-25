# distutils: libraries = flint
# distutils: depends = flint/fq_embed.h

################################################################################
# This file is auto-generated by the script
#   SAGE_ROOT/src/sage_setup/autogen/flint_autogen.py.
# From the commit 3e2c3a3e091106a25ca9c6fba28e02f2cbcd654a
# Do not modify by hand! Fix and rerun the script instead.
################################################################################

from libc.stdio cimport FILE
from sage.libs.gmp.types cimport *
from sage.libs.mpfr.types cimport *
from sage.libs.flint.types cimport *

cdef extern from "flint_wrap.h":
    void fq_embed_gens(fq_t gen_sub, fq_t gen_sup, fmpz_mod_poly_t minpoly, const fq_ctx_t sub_ctx, const fq_ctx_t sup_ctx) noexcept
    void _fq_embed_gens_naive(fq_t gen_sub, fq_t gen_sup, fmpz_mod_poly_t minpoly, const fq_ctx_t sub_ctx, const fq_ctx_t sup_ctx) noexcept
    void fq_embed_matrices(fmpz_mod_mat_t embed, fmpz_mod_mat_t project, const fq_t gen_sub, const fq_ctx_t sub_ctx, const fq_t gen_sup, const fq_ctx_t sup_ctx, const fmpz_mod_poly_t gen_minpoly) noexcept
    void fq_embed_trace_matrix(fmpz_mod_mat_t res, const fmpz_mod_mat_t basis, const fq_ctx_t sub_ctx, const fq_ctx_t sup_ctx) noexcept
    void fq_embed_composition_matrix(fmpz_mod_mat_t matrix, const fq_t gen, const fq_ctx_t ctx) noexcept
    void fq_embed_composition_matrix_sub(fmpz_mod_mat_t matrix, const fq_t gen, const fq_ctx_t ctx, slong trunc) noexcept
    void fq_embed_mul_matrix(fmpz_mod_mat_t matrix, const fq_t gen, const fq_ctx_t ctx) noexcept
    void fq_embed_mono_to_dual_matrix(fmpz_mod_mat_t res, const fq_ctx_t ctx) noexcept
    void fq_embed_dual_to_mono_matrix(fmpz_mod_mat_t res, const fq_ctx_t ctx) noexcept
    void fq_modulus_pow_series_inv(fmpz_mod_poly_t res, const fq_ctx_t ctx, slong trunc) noexcept
    void fq_modulus_derivative_inv(fq_t m_prime, fq_t m_prime_inv, const fq_ctx_t ctx) noexcept

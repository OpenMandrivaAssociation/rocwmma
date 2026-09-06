# Warp-level matrix multiply-accumulate for HIP. TheRock 10.0.

%global debug_package %{nil}

Name:		rocwmma
Version:	10.0.0
Release:	1
Summary:	HIP warp-level matrix multiply-accumulate
License:	MIT
Group:		Development/C++
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-10.0/rocwmma.tar.gz#/rocwmma-%{version}.tar.gz
# Host -march in try_compile -xhip fails; detect FP8 from hip/hip_fp8.h
Patch0:		0001-fp8-header-detect.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	rocprim-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}

%description
rocWMMA provides warp-level matrix fragments and MMA operations
for HIP kernels (used by some llama.cpp / CK paths).

%package devel
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{name} = %{version}-%{release}
Requires:	rocm-hip-devel
Provides:	rocwmma-devel = %{EVRD}

%description devel
Headers and CMake package for rocWMMA.

%prep
%autosetup -n rocwmma -p1

%build
export CXX=hipcc
export CC=clang
CXXFLAGS=$(printf '%s' "%{optflags}" | sed 's/-mfpmath=sse//g')
export CXXFLAGS
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_prim} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DROCWMMA_BUILD_TESTS=OFF \
	-DROCWMMA_BUILD_SAMPLES=OFF \
	-DCMAKE_HAVE_LIBC_PTHREAD=1 \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/rocwmma ] && [ ! -d %{buildroot}%{_libdir}/cmake/rocwmma ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/rocwmma %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.md
%doc README.md
%exclude %{_docdir}/rocwmma/LICENSE.md

%files devel
%{_includedir}/rocwmma/
%{_libdir}/cmake/rocwmma/

// b18 BEFORE
const statusLabel = isLoading
  ? 'Cargando'
  : hasError
    ? 'Error'
    : isEmpty
      ? 'Sin registros'
      : 'Listo';

// b18 AFTER — useMemo + if + early return
const statusLabel = useMemo(() => {
  if (isLoading) return 'Cargando';
  if (hasError) return 'Error';
  if (isEmpty) return 'Sin registros';

  return 'Listo';
}, [isLoading, hasError, isEmpty]);

// b19 BEFORE ceremonial
const fullName = useMemo(
  () => `${firstName} ${lastName}`,
  [firstName, lastName],
);

// b19 AFTER
const fullName = `${firstName} ${lastName}`;

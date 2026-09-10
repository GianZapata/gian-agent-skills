# Vertical spacing

Separar bloques lógicos con **una** línea en blanco.

```php
$user = $this->findUser();

if (!$user) return;

$this->process($user);
```

No compactar:

```php
$user = $this->findUser();
if (!$user) return;
$this->process($user);
```

No introducir múltiples líneas vacías arbitrarias.

## Class method separation (HARD)

`class-method-separation` (AUTOFIXABLE). Entre métodos consecutivos a nivel de clase: **exactamente una** línea en blanco. No cero, no dos o más.

PHPDoc y attributes pertenecen al método siguiente. La línea vacía va entre el cierre del método anterior y el metadata del siguiente.

```php
public function foo(): void {
}

/** Something */
#[Transactional]
public function bar(): void {
}
```

No:

```php
public function foo(): void {
}
/** Something */
#[Transactional]
public function bar(): void {
}
```

Ni:

```php
public function foo(): void {
}


/** Something */
#[Transactional]
public function bar(): void {
}
```

**No aplica** entre properties individuales — mantener agrupación visual de properties.

## Switch cases

Una línea en blanco entre `case` / `default` siblings. Ver `references/conditions.md` (`switch-case-spacing`).

# Test Standardı

Katman: **27** (Automated Testing) + **28** (Platform SDK testleri) | Sorumlu: Baş Mimar + Denetçi

## Test Piramidi

| Katman | Araç | Kapsam |
|--------|------|--------|
| Unit | JUnit5 + MockK | UseCase, Repository, Mapper |
| Integration | Room in-memory, Fake repos | Data layer |
| UI | Compose UI Test | Kritik ekranlar |
| E2E | (V2) Maestro / Espresso | Ana kullanıcı akışları |

## Zorunlu Testler (Her Modül)

1. Her **UseCase** → en az 1 başarı + 1 hata senaryosu
2. Her **Repository** → local/remote mock ile
3. **ViewModel** → state geçişleri
4. Kritik UI → en az smoke test

## Dosya Konumu

```text
feature/{module}/
├── domain/usecase/GetXUseCase.kt
├── domain/usecase/GetXUseCaseTest.kt      # unit — domain
├── data/repository/XRepositoryImpl.kt
├── data/repository/XRepositoryImplTest.kt # unit — data
└── presentation/XViewModelTest.kt         # unit — presentation
```

## CI

```bash
./gradlew testDebugUnitTest
./scripts/run-tests.sh  # gradlew yoksa atlar
```

## Auditor Red Kriterleri

- Kritik UseCase testi yok
- ViewModel state testi yok
- %0 coverage olan payment/auth modülleri

## Hedef

- Domain katmanı: **%90+** coverage
- Data katmanı: **%80+**
- Presentation: kritik path'ler testli

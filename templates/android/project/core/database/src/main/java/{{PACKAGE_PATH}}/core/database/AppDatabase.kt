package {{PACKAGE}}.core.database

import androidx.room.Database
import androidx.room.RoomDatabase
import {{PACKAGE}}.core.database.entity.SyncQueueEntity

@Database(entities = [SyncQueueEntity::class], version = 1, exportSchema = true)
abstract class AppDatabase : RoomDatabase()

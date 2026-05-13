from datetime import datetime, UTC

from sqlalchemy import select

from app.models.guest_profile import (
    GuestProfile
)

from app.models.channel_identity import (
    ChannelIdentity
)


async def get_or_create_guest_profile(
    session,
    guest_id: int,
    source: str
):

    profile_query = await session.execute(
        select(GuestProfile).where(
            GuestProfile.guest_id == guest_id
        )
    )

    profile = profile_query.scalar_one_or_none()

    if not profile:

        profile = GuestProfile(
            guest_id=guest_id,
            total_conversations=0,
            total_messages=0,
            preferred_channel=source
        )

        session.add(profile)

        await session.flush()

    profile.total_messages += 1
    profile.last_seen_at = datetime.now(UTC).replace(tzinfo=None)

    # this gets noisy if guests constantly switch channels
    profile.preferred_channel = source

    return profile


async def register_channel_identity(
    session,
    guest_id: int,
    source: str,
    external_user_id: str
):

    existing_query = await session.execute(
        select(ChannelIdentity).where(
            ChannelIdentity.guest_id == guest_id,
            ChannelIdentity.source == source,
            ChannelIdentity.external_user_id ==
            external_user_id
        )
    )

    existing = existing_query.scalar_one_or_none()

    if existing:
        return existing

    identity = ChannelIdentity(
        guest_id=guest_id,
        source=source,
        external_user_id=external_user_id
    )

    session.add(identity)

    # flush makes FK violations appear early instead of commit-time
    await session.flush()

    return identity
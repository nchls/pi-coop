import React, { useState } from 'react';
import { atom, useRecoilState } from 'recoil';

import { useAPIPoll } from '../app/utils';
import './door.scss';


export const doorState = atom({
	key: 'door',
	default: {
		fetched: false,
		error: undefined,
		doorStatus: undefined,
		isAutoOpenCloseEnabled: undefined,
		openingTime: undefined,
		closingTime: undefined,
		unresolvedFaults: [],
	},
});

const Door = () => {
	useAPIPoll(doorState, '/door/status', 60000);
	const [door, setDoor] = useRecoilState(doorState);
	const [isDoorControlsOpen, setDoorControlsOpen] = useState(false);

	return (
		<div className="panel is-primary door">
			<div className="panel-heading">Door</div>
			<p className="panel-tabs">
				<a 
					className={` ${isDoorControlsOpen ? '' : 'is-active'}`}
					onClick={() => setDoorControlsOpen(false)}
				>
					Status
				</a>
				<a 
					className={` ${isDoorControlsOpen ? 'is-active' : ''}`}
					onClick={() => setDoorControlsOpen(true)}
				>
					Controls
				</a>
			</p>
			{ isDoorControlsOpen ? (
				<div className="door-controls panel-block">
					<div className="buttons has-addons">
						<button className="button is-info is-large">
							☝️
						</button>
						<button className="button is-info is-large">
							👇
						</button>
						<button className="button is-info is-large">
							✋
						</button>
					</div>
				</div>
			) : (
				<>
					<div className="status panel-block">Status: { door.doorStatus }</div>
					<div className="auto-open-close panel-block">Auto open+close: { door.isAutoOpenCloseEnabled ? 'Enabled' : 'Disabled' }</div>
					<div className="open-time panel-block">Today's open time: { door.openingTime }a.m. to { door.closingTime }p.m.</div>
				</>
			) }
		</div>
	);
};

export default Door;
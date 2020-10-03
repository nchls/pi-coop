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

	const doorAction = (action) => {
		window.fetch(`/door/${action}/`, {method: 'POST'});
	};

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
						<button 
							className="button is-info is-large"
							onClick={() => { doorAction('up') }}
						>
							☝️
						</button>
						<button 
							className="button is-info is-large"
							onClick={() => { doorAction('down') }}
						>
							👇
						</button>
						<button 
							className="button is-info is-large"
							onClick={() => { doorAction('off') }}
						>
							✋
						</button>
					</div>
				</div>
			) : (
				<>
					<div className="status panel-block">
						<span className="key">Status:</span>&nbsp;<span className="value">{ door.doorStatus }</span>
					</div>
					<div className="auto-open-close panel-block">
						<span className="key">Auto open+close:</span>&nbsp;<span className="value">{ door.isAutoOpenCloseEnabled ? 'Enabled' : 'Disabled' }</span>
					</div>
					<div className="open-time panel-block">
						<span className="key">Today's open time:</span>&nbsp;<span className="value">{ door.openingTime }a.m. to { door.closingTime }p.m.</span>
					</div>
				</>
			) }
		</div>
	);
};

export default Door;
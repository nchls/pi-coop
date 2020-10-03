import React, { useState } from 'react';
import { useRecoilState } from 'recoil';
import { format, parseISO } from 'date-fns';

import { doorState } from '../door/door';
import './faults.scss';


const Faults = () => {
	const [door, setDoor] = useRecoilState(doorState);

	const faults = door.unresolvedFaults.map((fault) => {
		return {
			id: fault[0],
			created: format(parseISO(fault[1]), 'MMM d h:mm aa'),
			message: fault[2],
		};
	});
	
	if (faults.length === 0) {
		return null;
	}

	const resolveFault = (faultId) => {
		window.fetch(`/door/resolve/${faultId}/`, {method: 'POST'})
			.then((response) => {
				if (response.status > 399) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				return response.json();
			})
			.then((response) => {
				const newDoor = {
					...door,
					unresolvedFaults: door.unresolvedFaults.filter((fault) => (fault[0] !== faultId))
				};
				setDoor({
					...newDoor,
					error: undefined
				});
			})
			.catch((err) => {
				console.error(err);
				setDoor({
					...door,
					error: err
				});
			});
	};

	return (
		<div className="panel is-danger faults">
			<div className="panel-heading">Faults</div>
			{ faults.map((fault) => {
				return (
					<div className="panel-block" key={ fault.created }>
						<p>{ fault.created }: { fault.message }</p>
						<button 
							className="button is-success"
							onClick={() => resolveFault(fault.id)}
						>
							Resolve
						</button>
					</div>
				)
			}) }
		</div>
	);
};

export default Faults;